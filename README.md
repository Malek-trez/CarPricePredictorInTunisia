# Car Price Predictor in Tunisia

A machine learning project that predicts car prices in Tunisia based on various features and market data.

## Project Structure

```
├── Data/               # Contains datasets and raw data
├── Src/        
│   ├── Scraping/     # Web scraping scripts
│   ├── Modeling/     # ML models and training code
│   └── DataManip/    # Data preprocessing and manipulation
├── requirements.txt  
└── LICENSE       
```

## Features

- Web scraping of car listings from Tunisian car market websites
- Data preprocessing 
- Machine learning model for price prediction

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.