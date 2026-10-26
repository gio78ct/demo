import base64
import json
import os
import urllib.parse
import urllib.request

from .models import Offer


class Source:
    name = "base"

    def available(self):
        return True

    def search(self, query, limit=50):
        raise NotImplementedError


class EbaySource(Source):
    """eBay Browse API (ufficiale). Richiede EBAY_CLIENT_ID / EBAY_CLIENT_SECRET."""
    name = "ebay"

    def available(self):
        return bool(os.environ.get("EBAY_CLIENT_ID") and os.environ.get("EBAY_CLIENT_SECRET"))

    def _token(self):
        cred = f'{os.environ["EBAY_CLIENT_ID"]}:{os.environ["EBAY_CLIENT_SECRET"]}'
        req = urllib.request.Request(
            "https://api.ebay.com/identity/v1/oauth2/token",
            data=urllib.parse.urlencode({
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            }).encode(),
            headers={
                "Authorization": "Basic " + base64.b64encode(cred.encode()).decode(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.load(r)["access_token"]

    def search(self, query, limit=50):
        params = urllib.parse.urlencode({
            "q": query or "hard disk", "limit": min(limit, 200),
            "filter": "buyingOptions:{FIXED_PRICE},priceCurrency:EUR,conditions:{NEW}",
        })
        req = urllib.request.Request(
            "https://api.ebay.com/buy/browse/v1/item_summary/search?" + params,
            headers={"Authorization": "Bearer " + self._token(), "X-EBAY-C-MARKETPLACE-ID": "EBAY_IT"},
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            items = json.load(r).get("itemSummaries", [])
        out = []
        for it in items:
            if it.get("price", {}).get("currency") != "EUR":
                continue
            orig = it.get("marketingPrice", {}).get("originalPrice", {}).get("value")
            out.append(Offer.build(
                self.name, it["title"], it["price"]["value"], it["itemWebUrl"],
                image=it.get("image", {}).get("imageUrl"), original_price=orig,
            ))
        return out


# Amazon.it (Product Advertising API) e Trovaprezzi/idealo non hanno ancora un adapter:
# vedi README. Per aggiungerne uno basta una sottoclasse di Source registrata qui sotto.
SOURCES = {s.name: s for s in (EbaySource(),)}
