import requests
import json
import hashlib
import os
import time

class NorenAPI:
    def __init__(self):
        # Environment variables से credentials लें
        self.api_endpoint = os.environ.get('API_ENDPOINT', 'https://norenapi.shoonya.com/NorenWClientTP/')
        self.websocket_url = os.environ.get('WEBSOCKET_URL', 'wss://norenapi.shoonya.com/NorenWSTP/')
        self.access_token = None
        self.account_id = None
        self.user_id = os.environ.get('UID', 'FA45503')
        self.api_key = os.environ.get('API_KEY', '')
        self.secret_key = os.environ.get('SECRET_KEY', 'AZerLzHnn8cedLbn3QKoa6RIAQRO3bKpkkNpDKrNrOfBrPrHEpxgBcLcb1DB8Rke')
        self.client_id = os.environ.get('CLIENT_ID', 'FA45503_U')
        self.session = requests.Session()
        
    def get_login_url(self):
        """Generate OAuth login URL"""
        try:
            oauth_url = os.environ.get('OAUTH_URL', 'https://api.shoonya.com/NorenWClientTP/QuickAuth')
            login_url = f"{oauth_url}?api_key={self.api_key}"
            return {'status': 'success', 'url': login_url}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_access_token(self, auth_code):
        """Exchange auth code for access token"""
        try:
            secret_hash = hashlib.sha256(
                f"{self.secret_key}{auth_code}".encode()
            ).hexdigest()
            
            payload = {
                'api_key': self.api_key,
                'request_code': auth_code,
                'secret_key': secret_hash,
                'client_id': self.client_id,
                'uid': self.user_id,
                'source': 'API'
            }
            
            response = self.session.post(
                f"{self.api_endpoint}QuickAuth",
                json=payload
            )
            
            data = response.json()
            
            if data.get('stat') == 'Ok' or 'susertoken' in data:
                self.access_token = data.get('susertoken')
                self.account_id = data.get('actid')
                
                return {
                    'status': 'success',
                    'access_token': self.access_token,
                    'account_id': self.account_id,
                    'data': data
                }
            else:
                return {'status': 'error', 'message': data.get('emsg', 'Authentication failed')}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def make_request(self, endpoint, params=None):
        """Make authenticated API request"""
        try:
            if not self.access_token:
                return {'status': 'error', 'message': 'Not authenticated'}
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            if params is None:
                params = {}
            
            params['uid'] = self.user_id
            params['actid'] = self.account_id
            params['susertoken'] = self.access_token
            
            response = self.session.post(
                f"{self.api_endpoint}{endpoint}",
                json=params,
                headers=headers
            )
            
            return {'status': 'success', 'data': response.json()}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def get_quotes(self, exchange, tradingsymbol):
        return self.make_request('GetQuotes', {'exch': exchange, 'token': tradingsymbol})
    
    def search_scrip(self, search_text):
        return self.make_request('SearchScrip', {'stext': search_text, 'exch': 'NSE'})
    
    def place_order(self, order_params):
        return self.make_request('PlaceOrder', order_params)
    
    def modify_order(self, order_params):
        return self.make_request('ModifyOrder', order_params)
    
    def cancel_order(self, order_no):
        return self.make_request('CancelOrder', {'norenordno': order_no})
    
    def get_order_book(self):
        return self.make_request('OrderBook')
    
    def get_trade_book(self):
        return self.make_request('TradeBook')
    
    def get_single_order_history(self, order_no):
        return self.make_request('SingleOrdHist', {'norenordno': order_no})
    
    def get_holdings(self, product_type='C'):
        return self.make_request('Holdings', {'prd': product_type})
    
    def get_positions(self):
        return self.make_request('PositionBook')
    
    def get_limits(self):
        return self.make_request('Limits')
    
    def logout(self):
        try:
            response = self.make_request('Logout')
            self.access_token = None
            self.account_id = None
            return response
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
