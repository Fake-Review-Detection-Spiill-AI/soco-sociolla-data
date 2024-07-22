import requests
from typing import List
import csv
from urllib.parse import urlparse, parse_qs
from datetime import datetime


def scraper_soco(product_id: str) -> List[dict]:
    """
    this function is responsible to scrap data from review.soco.id
    """
    skip = 0
    limit = 6
    result = []
    while True:
        url = f"https://api.soco.id/reviews?skip={skip}&sort=-total_likes+-created_at&limit={limit}&filter=%7B%22is_published%22:true,%22elastic_search%22:true,%22product_id%22:%22{product_id}%22%7D"
        skip += limit
        try:
            payload = {}
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9,id;q=0.8',
                'cookie': 'SOCIOLLA_SESSION_ID=yzjw245o-tqu7-2meb-b8tm-fvizl62woq9c; _gid=GA1.2.1629435222.1721466527; sso_token=548f1fab649cd87f93ed73689ca432c204093444; _gcl_au=1.1.1793582362.1721466528; _hjSession_2179576=eyJpZCI6IjRiNjJkYzM0LTI5ZjYtNGI1ZS1hZDQ2LWI2ZTAxNzVhM2I3YiIsImMiOjE3MjE0NjY1MzMxMjEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _tt_enable_cookie=1; _ttp=gjng0UO_Gv88fkAJpYUvBsdv5QZ; _gat=1; _ga_363PMMDMHM=GS1.2.1721466531.1.1.1721466765.60.0.0; _ga_1LK3V2RBN2=GS1.1.1721466531.1.1.1721466766.0.0.0; _ga=GA1.1.272848259.1721466527; _hjSessionUser_2179576=eyJpZCI6IjdhMWVjNGVkLWEzOTEtNWZjMC04MWNlLWFhNzdiZTA2Zjk1NCIsImNyZWF0ZWQiOjE3MjE0NjY1MzMxMTksImV4aXN0aW5nIjp0cnVlfQ==',
                'origin': 'https://review.soco.id',
                'priority': 'u=1, i',
                'referer': 'https://review.soco.id/',
                'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Linux"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'soc-platform': 'review-web-desktop',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            response_json = response.json()
            response_data = response_json.get("data")
            if not response_data:
                return result

            for item in response_data :
                data_user = item.get("user")
                first_name = data_user.get("firstname")
                last_name = data_user.get("lastname")
                full_name = f"{first_name} {last_name}"
                review = item.get("details")
                duration_of_used = item.get("duration_of_used")
                rating = item.get("average_rating")
                date = item.get("created_at")
                source = item.get("source")
                data_product = item.get("product")
                product_name = data_product.get("name")
                temp_data = {
                    "name": full_name,
                    "rating": rating,
                    "lama_pemakaian": duration_of_used,
                    "date": date,
                    "review": review,
                    "source": source,
                    "product": product_name,
                }
                result.append(temp_data)
                print(f"Get review from {full_name}")

        except:
            break

    return result

def get_product_id(url):
    try:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        product_part = path_parts[3]
        product_id = product_part.split('-')[0] 
        if product_id:
            return product_id
        
    except:
        print("Product ID not found. Url not valid")
        exit()


def save_to_csv(data: List[dict], hastag=None) -> None:
    """
    this function responsible to save result of scraping to csv file
    """
    if not data:
        return
    
    file_name = f"output.csv"
    if hastag:
        file_name = f"output_{hastag}.csv"
    else:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        file_name = f"output_{formatted_datetime}.csv"

    keys = data[0].keys()
    with open(file_name, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

    print(f"Data saved to {file_name}")


if __name__ == "__main__":
    url = "https://review.soco.id/product/lip-balm/76782-pantenolips-lip-healbalm-lip-balm"
    product_id = get_product_id(url)
    result = scraper_soco(product_id)
    save_to_csv(result)
