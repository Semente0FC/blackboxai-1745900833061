
Built by https://www.blackbox.ai

---

```markdown
# Future MT5 Trading

Future MT5 Trading is a platform designed for automated trading operations using the MetaTrader 5 (MT5) trading terminal. The application implements various trading strategies and provides a user-friendly interface for managing trades, logs, and market analysis.

## Project Overview
The Future MT5 Trading application integrates sophisticated trading strategies based on technical indicators such as RSI, MACD, and Bollinger Bands, combined with a graphical user interface built using Tkinter. It allows users to connect to their MT5 accounts, select assets, set trade parameters, and manage their trading execution with real-time logging and updates.

## Installation

To run this project, ensure you have Python 3.x installed with the necessary packages. You can set up the environment by following these steps:

1. Clone the repository:
   ```bash
   git clone https://your-repository-url.git
   cd your-repository-directory
   ```

2. Install the required dependencies. Create a virtual environment and install the packages mentioned in `requirements.txt` or manually:
   ```bash
   pip install MetaTrader5 numpy pandas
   ```

3. Ensure that you have the MetaTrader 5 terminal installed and configured correctly on your machine.

4. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Upon launching the application, a splash screen will appear followed by a login screen.
2. Enter your MT5 server, account login, and password. Optionally, save the credentials for future use.
3. Once logged in, select assets, specify timeframes, and define the trading lot size from the dashboard.
4. Start or stop trading strategies for different assets using the provided controls.
5. Monitor the logs and trading status in real time on the interface.

## Features

- **Multi-Asset Trading**: Supports trading multiple assets simultaneously.
- **Dynamic Trading Strategies**: Configured to use a combination of indicators like EMA, RSI, MACD, and Bollinger Bands.
- **Real-Time Logging**: Keeps a detailed log of trading actions and errors for each asset.
- **User-Friendly Interface**: Built with Tkinter to provide an intuitive navigation experience.
- **Account Management**: Save and load login information for easier access to your MT5 account.
- **Risk Management**: Implements trading risk management strategies to ensure safer trading.

## Dependencies

The application relies on the following libraries:

- `MetaTrader5`: To connect and perform actions with the MT5 platform.
- `numpy`: For numerical operations.
- `pandas`: For data manipulation and analysis.

These dependencies are specified in the project and can be installed via pip as mentioned above.

## Project Structure

```
.
├── main.py          # Entry point of the application
├── estrategia.py    # Contains the trading strategy implementation
├── log_system.py    # Handles logging of events and errors
├── login.py         # GUI for user login
├── painel.py        # Main trading dashboard and controls
├── splash_screen.py  # Splash screen implementation
├── utils.py         # Utility functions for login and asset management
└── requirements.txt  # List of dependencies (if applicable)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This application is powered by the MetaTrader 5 API and development tools provided by MetaQuotes. Thanks to the contributors who provide support and resources for this project.
```