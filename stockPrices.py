import requests, json, os


class StockPrice:
    def __init__(self, api_key=None, verbose=False, base_url="https://finnhub.io/api/v1"):
        self.api_key = api_key
        self.verbose = verbose
        self.base_url = base_url
        self.companyKeys = {}
        self.load_company_symbols()
    
    def get_api_key(self):
        # check to see if api key exist in env 
        if not self.api_key:
            self.api_key = os.environ.get('FINNHUB_API_KEY')
        if not self.api_key:
            raise ValueError("API Key not set. Please provide a valid API key.")
        return self.api_key

    def load_company_symbols(self, fileName="symbols.json"):
        if not os.path.exists(fileName):
            raise FileNotFoundError("Missing symbols.json file.")
        with open(fileName,'r') as f:
            self.companyKeys = json.load(f)
        return
    def debug(self, s):
        if self.verbose:
            print(s)
    def get_symbol(self, s):

        s = s.strip().lower()

        for item in self.companyKeys:
            symbol = item.get('s', '').lower()
            name = item.get('n', '').lower()

            # Exact match on symbol or name
            if s == symbol or s == name:
                return item.get('s')  # Return original symbol (case preserved)

        # Partial match as fallback
        for item in self.companyKeys:
            symbol = item.get('s', '').lower()
            name = item.get('n', '').lower()

            if s in symbol or s in name:
                return item.get('s')

        return None  # not found
    def get_name_from_symbol(self, symbol):
        symbol = symbol.strip().lower()

        for item in self.companyKeys:
            if item.get('s', '').lower() == symbol:
                return item.get('n')
        return None

    def get_stockPrice(self, company):

        # early check for api key
        if not self.api_key:
            self.get_api_key()

        symbol = self.get_symbol(company)

        if symbol:
            url = f"{self.base_url}/quote"
            params = {
                "symbol": symbol,
                "token": self.api_key
            }

            response = requests.get(url, params=params)

            self.debug(f"HTTP Response Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                return data.get('c')  # current price
            elif response.status_code == 429:
                print(f"Rate limit met, try again later")
            else:
                return None
        else:
            return 'Unable to locate company/Symbol'