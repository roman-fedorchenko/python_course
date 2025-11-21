import yfinance as yf                               # бібліотека для завантаження фінансових даних
import pandas as pd                                 # бібліотека для роботи з таблицями
import numpy as np                                  # бібліотека для наукових обчислень
import matplotlib.pyplot as plt                     # бібліотека для візуалізації
from scipy.optimize import minimize, curve_fit      # бібліотека для оптимізації та підгонки кривих
from scipy.signal import savgol_filter              # бібліотека для обробки сигналів
from scipy.stats import norm                        # бібліотека для статистичних розподілів
import os                                           # бібліотека для роботи з операційною системою
import seaborn as sns                               # бібліотека для покращеної візуалізації
import sys                                          # бібліотека для роботи з системними функціями
import json                                         # бібліотека для роботи з JSON файлами

# Шляхи
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))        # Поточний каталог скрипта
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")          # Файл конфігурації
FILE_RAW = os.path.join(SCRIPT_DIR, "data_high_precision.csv") # Файл з сирими даними
FILE_RF = os.path.join(SCRIPT_DIR, "data_risk_free.csv")       # Файл з безризиковою ставкою
FILE_PLOT = os.path.join(SCRIPT_DIR, "final_dashboard.png")    # Файл з дашбордом
FILE_REPORT = os.path.join(SCRIPT_DIR, "final_report.txt")     # Файл зі звітом

# завантаження конфігурації з JSON
def load_config(path):
    # 1. Визначаємо стандартні дані (резервний варіант)
    default_config = {
        "tickers": ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA', 'TSLA', 'META', 'AMD'],
        "risk_free_ticker": "^TNX",
        "start_date": "2017-01-01",
        "end_date": "2024-01-01"
    }

    try:
        # 2. Спроба відкрити файл
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ Налаштування завантажено з файлу: {path}")
        return data

    except FileNotFoundError:
        # 3. Якщо файлу немає — не падаємо, а повідомляємо і беремо стандарт
        print(f"⚠️ Файл {path} не знайдено. Використовуються стандартні налаштування.")
        return default_config

    except json.JSONDecodeError:
        # 4. Якщо файл пошкоджений (не JSON) — те саме
        print(f"⚠️ Помилка читання JSON у файлі {path}. Використовуються стандартні налаштування.")
        return default_config
    
# завантаження конфігурації
config = load_config(CONFIG_PATH)
TICKERS = config["tickers"]
RISK_FREE_TICKER = config["risk_free_ticker"]
START_DATE = config["start_date"]
END_DATE = config["end_date"]

plt.style.use('ggplot')

# завантаження даних з Yahoo Finance або локального файлу
def get_data():
    print(f"\nЗавантаження даних")
    if os.path.exists(FILE_RAW):
        print("Знайдено локальний файл даних.")
        df = pd.read_csv(FILE_RAW, index_col=0, parse_dates=True)
    else:
        print("Завантаження акцій з Yahoo Finance...")
        df = yf.download(TICKERS, start=START_DATE, end=END_DATE, auto_adjust=True)['Close']
        df.to_csv(FILE_RAW)
    
    # Безризикова ставка
    if os.path.exists(FILE_RF):
        rf_df = pd.read_csv(FILE_RF, index_col=0, parse_dates=True)
        col_name = 'Close' if 'Close' in rf_df.columns else rf_df.columns[0]
        rf_series = rf_df[col_name]
    else:
        print("Завантаження ставки (^TNX)...")
        rf_data = yf.download(RISK_FREE_TICKER, start=START_DATE, end=END_DATE, auto_adjust=True)
        if isinstance(rf_data, pd.DataFrame):
            rf_series = rf_data['Close'] if 'Close' in rf_data.columns else rf_data.iloc[:, 0]
        else:
            rf_series = rf_data
        rf_series = rf_series / 100
        rf_series.name = "Close"
        rf_series.to_csv(FILE_RF)

    avg_rf = float(rf_series.mean())
    print(f"Дані успішно завантажено. Активів: {len(df.columns)}. Ставка: {avg_rf:.2%}")
    return df, avg_rf

# оптимізація портфелю (макс. Шарп). Використання SCIPY.OPTIMIZE.MINIMIZE
def optimize_portfolio(prices_df, risk_free_rate):
    print(f"\nОптимізація портфелю (Max Sharpe)")
    log_returns = np.log(prices_df / prices_df.shift(1)).dropna()
    mean_returns = log_returns.mean() * 252
    cov_matrix = log_returns.cov() * 252
    num_tickers = len(prices_df.columns)

    def negative_sharpe(weights):
        p_ret = np.sum(mean_returns * weights)
        p_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return -((p_ret - risk_free_rate) / p_vol)

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_tickers))
    init_guess = [1/num_tickers] * num_tickers

    options = {'ftol': 1e-15, 'maxiter': 10000000}
    result = minimize(negative_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=constraints, tol=1e-15, options=options)
    
    return result.x, log_returns, mean_returns, cov_matrix

# моделювання тренду росту капіталу. Використання SCIPY.OPTIMIZE.CURVE_FIT
def get_trend_data(log_returns, optimal_weights):
    portfolio_log_ret = log_returns.dot(optimal_weights)
    cumulative_ret = np.exp(portfolio_log_ret.cumsum())
    y_data = cumulative_ret.values
    x_data = np.arange(len(y_data))

    def growth_model(t, a, b):
        return a * np.exp(b * t)
    try:
        params, _ = curve_fit(growth_model, x_data, y_data, p0=[1, 0.0005], method='trf')
        y_fit = growth_model(x_data, *params)
    except:
        print("Не вдалося побудувати тренд (curve_fit error).")
        y_fit = y_data 
        
    return cumulative_ret, y_fit

# технічний аналіз: фільтрація шумів за допомогою Фільтру Савицького-Голея. Використання SCIPY.SIGNAL.SAVGOL_FILTER
def technical_analysis_signal(prices_df):
    ticker = input("\nВведіть тікер для тех. аналізу (напр. TSLA): ").upper()
    if ticker not in prices_df.columns:
        print("Тікер не знайдено в даних.")
        return

    print(f"Технічний аналіз (Фільтр Савицького-Голея)")
    y_data = prices_df[ticker].values
    
    # Фільтрація шуму: window_length=51, polyorder=3
    try:
        y_smooth = savgol_filter(y_data, window_length=51, polyorder=3)
    except:
        # Якщо даних мало, зменшуємо вікно
        y_smooth = savgol_filter(y_data, window_length=11, polyorder=2)

    plt.figure(figsize=(12, 6))
    plt.plot(prices_df.index, y_data, label='Реальна ціна (з шумом)', alpha=0.4, color='gray')
    plt.plot(prices_df.index, y_smooth, label='SciPy Trend (Clean)', color='blue', linewidth=2)
    plt.title(f'Фільтрація ринкового шуму: {ticker}')
    plt.xlabel('Дата')
    plt.ylabel('Ціна ($)')
    plt.legend()
    plt.show()

# оцінка ризиків портфелю за допомогою Value at Risk (VaR). Використання SCIPY.STATS.NORM
def calculate_risk_metrics(prices_df, optimal_weights):
    print(f"\nАналіз ризиків (Value at Risk)")
    
    returns = prices_df.pct_change().dropna()
    portfolio_returns = returns.dot(optimal_weights)
    
    # 1. Підгонка нормального розподілу (Fit)
    mu, std = norm.fit(portfolio_returns)
    
    # 2. Розрахунок VaR 95% (Percent Point Function)
    # Це число показує межу: "у 95% випадків збиток не перевищить X"
    var_95 = norm.ppf(0.05, mu, std)
    
    print(f"Середній денний дохід: {mu:.4%}")
    print(f"Волатильність (Sigma): {std:.4%}")
    print(f"VaR (95%): {var_95:.2%} (Макс. денний збиток з імовірністю 95%)")
    
    plt.figure(figsize=(10, 6))
    # Гістограма
    plt.hist(portfolio_returns, bins=50, density=True, alpha=0.6, color='green', label='Реальні доходи')
    
    # Крива розподілу (PDF)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2, label='SciPy Norm Fit')
    
    # Лінія ризику
    plt.axvline(var_95, color='red', linestyle='--', label=f'VaR 95%: {var_95:.2%}')
    
    plt.title('Розподіл прибутків та оцінка ризику (VaR)')
    plt.legend()
    plt.show()

# візуалізація дашборду з трьома графіками
def visualize_dashboard(optimal_weights, mean_rets, cov_mat, cum_ret, y_trend, rf_rate, tickers):
    print(f"\nПобудова дашборду")
    fig = plt.figure(figsize=(16, 10))
    
    # 1. Pie Chart
    ax1 = plt.subplot2grid((2, 2), (0, 0))
    mask = optimal_weights > 0.001 
    labels = [t for t, w in zip(tickers, optimal_weights) if w > 0.001]
    sizes = optimal_weights[mask]
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    ax1.set_title('Оптимальний розподіл')

    # 2. Trend
    ax2 = plt.subplot2grid((2, 2), (0, 1))
    ax2.plot(cum_ret.index, cum_ret.values, label='Історія', alpha=0.7)
    ax2.plot(cum_ret.index, y_trend, 'r--', label='SciPy Тренд', linewidth=2)
    ax2.set_title('Ріст капіталу')
    ax2.legend()

    # 3. Efficient Frontier
    ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)
    n_samples = 2000
    results = np.zeros((3, n_samples))
    for i in range(n_samples):
        w = np.random.random(len(tickers))
        w /= np.sum(w)
        p_ret = np.sum(mean_rets * w)
        p_vol = np.sqrt(np.dot(w.T, np.dot(cov_mat, w)))
        results[0,i] = p_vol
        results[1,i] = p_ret
        results[2,i] = (p_ret - rf_rate) / p_vol

    sc = ax3.scatter(results[0,:], results[1,:], c=results[2,:], cmap='viridis', s=10, alpha=0.5)
    plt.colorbar(sc, label='Sharpe', ax=ax3)
    
    opt_ret = np.sum(mean_rets * optimal_weights)
    opt_vol = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_mat, optimal_weights)))
    ax3.scatter(opt_vol, opt_ret, c='red', s=150, label='Оптимум')
    ax3.set_title('Ефективний фронт')
    ax3.legend()

    plt.tight_layout()
    plt.show() 
    fig.savefig(FILE_PLOT)
    print(f"Графік збережено у {FILE_PLOT}")
    return opt_ret, opt_vol

# аналіз сезонності за місяцями. Використання теплової карти (Heatmap)
def analyze_monthly_seasonality(prices_df):
    ticker = input("\nВведіть тікер для аналізу (напр. AAPL): ").upper()
    if ticker not in prices_df.columns:
        print(f"Помилка: Тікер {ticker} відсутній.")
        return

    print(f"Аналіз сезонності: {ticker}")
    try:
        monthly_prices = prices_df[ticker].resample('ME').last()
    except:
        monthly_prices = prices_df[ticker].resample('M').last()
        
    monthly_returns = monthly_prices.pct_change() * 100
    seasonality_df = pd.DataFrame({
        'Returns': monthly_returns,
        'Year': monthly_returns.index.year,
        'Month': monthly_returns.index.month
    })
    
    pivot_table = seasonality_df.pivot_table(values='Returns', index='Year', columns='Month')
    
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="RdYlGn", center=0)
    plt.title(f'Сезонність {ticker} (%)')
    plt.show()
# матриця кореляції активів
def plot_correlation_matrix(prices_df):
    print("\nМатриця кореляції")
    plt.figure(figsize=(10, 8))
    sns.heatmap(prices_df.pct_change().corr(), annot=True, cmap='coolwarm', fmt=".3f")
    plt.title("Кореляція активів")
    plt.show()
# генерація текстового звіту
def generate_report(tickers, weights, ret, vol, sharpe):
    with open(FILE_REPORT, "w", encoding="utf-8") as f:
        f.write("ФІНАНСОВИЙ ЗВІТ\n" + "="*30 + "\n")
        f.write(f"Прибуток (Log): {ret:.4f}\nВолатильність: {vol:.4f}\nШарп: {sharpe:.4f}\n\n")
        f.write("Розподіл:\n")
        for t, w in zip(tickers, weights):
            if w > 0.001: f.write(f"{t}: {w*100:.2f}%\n")
    print(f"Звіт збережено у {FILE_REPORT}")

# Головне меню
def main_menu():
    prices = None       # для збереження цін
    rf_rate = None      # для збереження безризикової ставки
    opt_weights = None  # для збереження оптимальних ваг
    
    while True:
        print("\n" + "="*42)
        print("   ФІНАНСОВИЙ АНАЛІЗАТОР (SCIPY)   ")
        print("="*42)
        
        # Динамічний статус
        data_status = "✅ Є" if prices is not None else "❌ НЕМАЄ"
        opt_status = "✅ Є" if opt_weights is not None else "❌ НЕМАЄ"
        
        print(f"Статус даних: {data_status} | Оптимізація: {opt_status}")
        print("-" * 42)
        print("1. Завантажити/Оновити дані")
        print("2. Повна оптимізація (scipy.optimize)")
        print("3. Технічний аналіз: Фільтр шумів (scipy.signal)")
        print("4. Оцінка ризику VaR (scipy.stats)")
        print("5. Аналіз сезонності (Heatmap)")
        print("6. Матриця кореляції активів")
        print("7. Список доступних активів")
        print("0. Вихід")
        
        choice = input("\nВаш вибір: ")

        if choice == '0':
            print("Роботу завершено.")
            sys.exit()

        elif choice == '1':
            try:
                prices, rf_rate = get_data()
                opt_weights = None # Скидаємо стару оптимізацію, бо дані змінились
            except Exception as e:
                print(f"Помилка завантаження: {e}")

        elif choice == '2': # OPTIMIZE
            if prices is None:
                print("⚠️ Спочатку завантажте дані (Пункт 1)")
                continue
            w, logs, means, covs = optimize_portfolio(prices, rf_rate)
            opt_weights = w
            cum_ret, y_trend = get_trend_data(logs, w)
            fin_ret, fin_vol = visualize_dashboard(w, means, covs, cum_ret, y_trend, rf_rate, prices.columns)
            generate_report(prices.columns, w, fin_ret, fin_vol, (fin_ret - rf_rate)/fin_vol)

        elif choice == '3': # SIGNAL
            if prices is None:
                print("⚠️ Спочатку завантажте дані (Пункт 1)")
                continue
            technical_analysis_signal(prices)

        elif choice == '4': # STATS
            if prices is None:
                print("⚠️ Спочатку завантажте дані (Пункт 1)")
                continue
            if opt_weights is None:
                print("⚠️ Спочатку виконайте оптимізацію (Пункт 2), щоб сформувати портфель!")
                continue
            calculate_risk_metrics(prices, opt_weights)

        elif choice == '5': # SEASONALITY
            if prices is None:
                print("⚠️ Спочатку завантажте дані")
                continue
            analyze_monthly_seasonality(prices)

        elif choice == '6': # CORRELATION MATRIX
            if prices is None:
                print("⚠️ Спочатку завантажте дані")
                continue
            plot_correlation_matrix(prices)
            
        elif choice == '7': # LIST ASSETS
            if prices is None:
                print("⚠️ Дані відсутні")
            else:
                print("\nАктиви:", ", ".join(prices.columns))

        else:
            print("Невірний вибір.")

if __name__ == "__main__":
    main_menu()