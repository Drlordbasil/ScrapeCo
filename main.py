import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Class for automated data collection using web scraping
class WebScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def scrape_data(self, url):
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup


# Class for scraping e-commerce websites and extracting product information
class EcommerceScraper:
    def __init__(self):
        self.web_scraper = WebScraper()

    def scrape_product_info(self, url):
        soup = self.web_scraper.scrape_data(url)

        product_name = soup.find("h1", class_="product-name").text.strip()
        price = soup.find("span", class_="price").text.strip()
        description = soup.find("div", class_="description").text.strip()
        availability = soup.find("span", class_="availability").text.strip()

        return product_name, price, description, availability


# Class for cleaning and formatting scraped data
class DataCleaner:
    @staticmethod
    def clean_price(price):
        price = re.sub(r"[^\d.]", "", price)
        return float(price)

    @staticmethod
    def format_price(price):
        return "{:.2f}".format(price)

    @staticmethod
    def clean_description(description):
        description = re.sub(r"<.*?>", "", description)
        return description


# Class for competitive pricing analysis
class PricingAnalyzer:
    def __init__(self):
        self.data_cleaner = DataCleaner()

    def analyze_pricing_trends(self, prices):
        avg_price = np.mean(prices)
        min_price = np.min(prices)
        max_price = np.max(prices)

        return avg_price, min_price, max_price

    def pricing_strategy(self, prices):
        if len(prices) > 0:
            min_price = np.min(prices)
            max_price = np.max(prices)
            if max_price - min_price >= 10:
                return "Price gap too wide, consider adjusting"
            else:
                return "Price gap within acceptable range"
        else:
            return "No pricing data available"


# Class for price comparison and alerting
class PriceComparator:
    @staticmethod
    def compare_prices(product, urls):
        prices = []
        ecommerce_scraper = EcommerceScraper()
        for url in urls:
            product_name, price, description, availability = ecommerce_scraper.scrape_product_info(url)
            cleaned_price = DataCleaner.clean_price(price)
            prices.append(cleaned_price)

        avg_price, min_price, max_price = PricingAnalyzer().analyze_pricing_trends(prices)

        # Price variation alert
        if max_price - min_price >= 10:
            PriceComparator.send_price_alert(product, urls)

        return avg_price, min_price, max_price

    @staticmethod
    def send_price_alert(product, urls):
        message = f"Price variation alert for {product}:\n\n"
        ecommerce_scraper = EcommerceScraper()
        for url in urls:
            product_name, price, description, availability = ecommerce_scraper.scrape_product_info(url)
            message += f"Product: {product_name}\nPrice: {price}\n\n"

        # Email notification
        email_notifier = EmailNotifier()
        email_notifier.send_email("Price Variation Alert", message)


# Class for historical data tracking
class HistoricalDataTracker:
    def __init__(self):
        self.historical_data = {}

    def track_data(self, product, price):
        if product in self.historical_data:
            self.historical_data[product].append(price)
        else:
            self.historical_data[product] = [price]

    def analyze_data(self, product):
        if product in self.historical_data:
            prices = self.historical_data[product]
            avg_price, min_price, max_price = PricingAnalyzer().analyze_pricing_trends(prices)

            # Visualize historical pricing trends
            plt.plot(prices)
            plt.xlabel("Time")
            plt.ylabel("Price")
            plt.title(f"Historical Pricing Trends - {product}")
            plt.show()
        else:
            print("No historical data available for the product")


# Class for user-friendly dashboard
class Dashboard:
    def __init__(self):
        self.product_urls = {}

    def add_product(self, product, urls):
        self.product_urls[product] = urls

    def view_scraped_data(self, product):
        urls = self.product_urls.get(product, [])
        if urls:
            ecommerce_scraper = EcommerceScraper()
            for url in urls:
                product_name, price, description, availability = ecommerce_scraper.scrape_product_info(url)
                print(f"Product: {product_name}\nPrice: {price}\nDescription: {description}\nAvailability: {availability}\n")
        else:
            print("No data available for the product")

    def visualize_pricing_trends(self, product):
        urls = self.product_urls.get(product, [])
        if urls:
            prices = []
            ecommerce_scraper = EcommerceScraper()
            for url in urls:
                product_name, price, description, availability = ecommerce_scraper.scrape_product_info(url)
                cleaned_price = DataCleaner.clean_price(price)
                prices.append(cleaned_price)

            plt.plot(prices)
            plt.xlabel("Time")
            plt.ylabel("Price")
            plt.title(f"Pricing Trends - {product}")
            plt.show()
        else:
            print("No data available for the product")


# Class for email notifications
class EmailNotifier:
    @staticmethod
    def send_email(subject, message):
        sender_email = "sender@example.com"
        sender_password = "password"
        receiver_email = "receiver@example.com"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()


# Main program execution
if __name__ == "__main__":
    ecommerce_urls = ["https://www.example.com/product1", "https://www.example.com/product2"]

    dashboard = Dashboard()
    dashboard.add_product("Product 1", ecommerce_urls)
    dashboard.view_scraped_data("Product 1")
    dashboard.visualize_pricing_trends("Product 1")

    price_comparator = PriceComparator()
    price_comparator.compare_prices("Product 1", ecommerce_urls)