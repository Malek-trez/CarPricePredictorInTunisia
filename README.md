# Car Price Predictor in Tunisia

A machine learning project that predicts car prices in Tunisia based on various features and market data.

## Project Structure

```
├── Data/               # Contains datasets and raw data
├── Src/               # Source code
│   ├── Scraping/     # Web scraping scripts
│   ├── Modeling/     # ML models and training code
│   └── DataManip/    # Data preprocessing and manipulation
├── requirements.txt   # Project dependencies
└── LICENSE           # Project license
```

## Features

- Web scraping of car listings from Tunisian car market websites
- Data preprocessing and feature engineering
- Machine learning model for price prediction
- Data visualization and analysis
- Interactive price prediction interface

## Requirements

- Python 3.x
- beautifulsoup4==4.12.3
- Requests==2.32.3
- seaborn==0.13.2
- matplotlib==3.9.2
- scikit-learn==1.5.1

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Malek-trez/CarPricePredictorInTunisia.git
cd CarPricePredictorInTunisia
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Data Collection:
   - Run the scraping scripts in the `Src/Scraping` directory to collect car data
   - The collected data will be stored in the `Data` directory

2. Data Processing:
   - Use the scripts in `Src/DataManip` to preprocess and prepare the data
   - Generate feature engineering and data cleaning

3. Model Training:
   - Navigate to `Src/Modeling` to train the price prediction model
   - The trained model will be saved for future predictions

4. Making Predictions:
   - Use the trained model to predict car prices based on input features
   - View visualizations and analysis of the predictions

## License

This project is licensed under the terms included in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
