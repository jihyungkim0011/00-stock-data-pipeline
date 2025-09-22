import FinanceDataReader as fdr
import yfinance as yf
import os

def fetch_nasdaq_companies_field():
    """
    Fetches NASDAQ company listings using a hybrid approach:
    - fdr for Name, Symbol, Industry.
    - yfinance for Sector.
    Saves the combined data to a CSV file.
    """
    print("Fetching initial company data from FinanceDataReader...")
    try:
        # 1. Get base data from fdr
        nasdaq_fdr = fdr.StockListing('NASDAQ')
        
        # Select relevant columns and drop rows with missing essential data
        nasdaq_df = nasdaq_fdr[['Symbol', 'Name', 'Industry']].dropna().reset_index(drop=True)
        
        symbols = nasdaq_df['Symbol'].tolist()
        print(f"Found {len(symbols)} companies. Now fetching 'Sector' info from yfinance...")
        print("This process can still take a significant amount of time.")

        # 2. Get Sector from yfinance for each symbol
        sectors = []
        for i, symbol in enumerate(symbols):
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                sector = info.get('sector', 'N/A') # Provide a default value
                sectors.append(sector)
            except Exception as e:
                print(f"{e}: {symbol} failed to fetch - skipping.")
                sectors.append('N/A') # Append default value on error
            
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1}/{len(symbols)} symbols for Sector info...")

        # 3. Add the sectors list as a new column to the DataFrame
        nasdaq_df['Sector'] = sectors
        
        # Reorder columns for clarity
        nasdaq_df = nasdaq_df[['Symbol', 'Name', 'Sector', 'Industry']]

        # 4. Save to CSV
        output_dir = 'data'
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, 'nasdaq_companies_hybrid.csv')

        nasdaq_df.index.name = 'id'
        nasdaq_df.to_csv(output_path, index=True, encoding='utf-8')

        print(f"\nSuccessfully saved combined company data to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_nasdaq_companies_field()
