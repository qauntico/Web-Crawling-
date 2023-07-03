import scrapy
import json


class TherapistSpider(scrapy.Spider):
    name = "therapist"
    allowed_domains = ["www.amtamassage.org"]
    start_urls = ["https://www.amtamassage.org/find-massage-therapist/?page=1/"]
    
    currentpage = 1
    json_data = {
    'CurrentPage': 1,
    'Location': '',
    'Keyword': '',
    'ResourceType': 'therapist',
    }
    headers = {
    'authority': 'www.amtamassage.org',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,en-US;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': '_gcl_au=1.1.2096145420.1679340326; _gid=GA1.2.408236631.1679340329; sa-user-id=s%253A0-fa99c640-362f-4954-7bdf-26222653bce1.hgUvqkO8hzh5HoHu1VPj6zn%252BOI69EZWPOtr08knnOLY; sa-user-id-v2=s%253A-pnGQDYvSVR73yYiJlO84Q.E2R1OJglgka6SNo0CCHltmYTSpVRKrdXzQbjRbPCeyE; _fbp=fb.1.1679340329192.2056025830; ASP.NET_SessionId=pc220edqh4jkmbwbptgp4in3; ln_or=eyIzMTU4NjYiOiJkIn0%3D; _clck=pbjoh0|1|fa5|0; iv=76b45aa9-b73b-454f-afee-74849ce7466d; _uetsid=f8f9b790c75411eda4f74349abfcb144; _uetvid=f8faf1c0c75411eda809cf729bbfe695; _ga=GA1.2.1891063821.1679340328; _ga_ZVHSW3DBTW=GS1.1.1679600096.13.0.1679600096.60.0.0',
    'origin': 'https://www.amtamassage.org',
    'referer': 'https://www.amtamassage.org/find-massage-therapist/?page=1',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    }
    
    link = "https://www.amtamassage.org/api/v1/famr/getMassageResources"
    def start_requests(self):
        yield scrapy.Request(url=self.link, method="POST", body=json.dumps(self.json_data), headers=self.headers, callback=self.parse)

    def parse(self, response):
        dic = {}
        page = json.loads(response.body)
        page_data = page.get('massageResources')
        for data in page_data:
            name = data.get('resourceName')
            address = data.get('officeAddressLine1')
            link = response.urljoin(data.get('urlToDetailsPage'))
            if data.get('officeAddressLine1') != "" :
                second_address = data.get('officeAddressLine1')
                yield scrapy.Request(url=link, callback=self.parse_profile, meta={'name':name,'address':address,'second_address':second_address})
            else:
                second_address = "#########"
                yield scrapy.Request(url=link, callback=self.parse_profile, meta={'name':name,'address':address,'second_address':second_address})
        self.currentpage += 1
        if self.currentpage < 4:
            json_data2 = {
                'CurrentPage': self.currentpage,
                'Location': '',
                'Keyword': '',
                'ResourceType': 'therapist',
                }
            yield scrapy.Request(url=self.link, method="POST", body=json.dumps(json_data2),headers=self.headers, callback=self.parse)
            


    def parse_profile(self, response):
        name = response.request.meta['name']
        address = response.request.meta['address']
        second_address = response.request.meta['second_address']
        number = response.xpath("//div[@class='amta-flex-grow-5 amta-padding-bottom-1']/p/span/a/text()").get()
        yield {
            'name':name,
            'address':address,
            'second_address':second_address,
            'number':number
        }