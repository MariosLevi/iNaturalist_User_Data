import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv


full_months = {"Jan":"January", "Feb":"February", "Mar":"March","Apr":"April","May":"May","Jun":"June","Jul":"July","Aug":"August","Sep":"September","Oct":"October","Nov":"November","Dec":"December"}

#using a list of countries in this case
list_of_usernames = ['Afghanistan','Albania','Algeria','American Samoa','Andorra','Angola','Anguilla','AntiguaandBarbuda','Argentina','Armenia','Aruba','Australia','Austria','Azerbaijan','Bahrain','Bahamas','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bermuda','Bhutan','Bolivia','Bonaire','BosniaandHerzegovina','Botswana','Bouvet Island','Brazil','Brunei','Bulgaria','Burkina Faso','Burundi','Cambodia','Cameroon','Canada','CapeVerde','CaymanIslands','CentralAfricanRepublic','Chad','Chile','China','ChristmasIsland','CocosIslands','Colombia','Comoros','Congo','CookIslands','CostaRica','CotedIvoire','Croatia','Cuba','Curacao','Cyprus','CzechRepublic','Denmark','Djibouti','Dominica','DominicanRepublic','Ecuador','Egypt','El Salvador','EquatorialGuinea','Eritrea','Estonia','Ethiopia','FalklandIslands','FaroeIslands','Fiji','Finland','France','FrenchGuiana','FrenchPolynesia','Gabon','Gambia','Georgia','Germany','Ghana','Gibraltar','Greece','Greenland','Grenada','Guadeloupe','Guam','Guatemala','Guernsey','Guinea','Guyana','Haiti','Vatican','Honduras','HongKong','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland','IsleofMan','Israel','Italy','Jamaica','Japan','Jersey','Jordan','Kazakhstan','Kenya','Kiribati','NorthKorea','SouthKorea','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya','Liechtenstein','Lithuania','Luxembourg','Macao','NorthernMacedonia','Madagascar','Malawi','Malaysia','Maldives','Mali','Malta','MarshallIslands','Martinique','Mauritania','Mauritius','Mayotte','Mexico','Micronesia','Moldova','Monaco','Mongolia','Montenegro','Montserrat','Morocco','Mozambique','Myanmar','Namibia','Nauru','Nepal','Netherlands','NewCaledonia','NewZealand','Nicaragua','Niger','Nigeria','Niue','NorfolkIsland','NorthernMarianaIslands','Norway','Oman','Pakistan','Palau','Palestine','Panama','PapuaNewGuinea','Paraguay','Peru','Philippines','Pitcairn','Poland','Portugal','PuertoRico','Qatar','Romania','Russia','Rwanda','SaintKittsandNevis','SaintLucia','SaintMartin','SaintPierreandMiquelon','SaintVincentandtheGrenadines','Samoa','SanMarino','SaoTomeandPrincipe','SaudiArabia','Senegal','Serbia','Seychelles','SierraLeone','Singapore','SintMaarten','Slovakia','Slovenia','SolomonIslands','Somalia','SouthAfrica','SouthSudan','Spain','SriLanka','Sudan','Suriname','SvalbardandJanMayen','Swaziland','Sweden','Switzerland','Syria','Taiwan','Tajikistan','Tanzania','Thailand','Togo','Tonga','TrinidadandTobago','Tunisia','Turkey','Turkmenistan','TurksandCaicos','Tuvalu','Uganda','Ukraine','UnitedArabEmirates','UnitedKingdom','UnitedStates','Uruguay','Uzbekistan','Vanuatu','Venezuela','Vietnam','VirginIslands','WesternSahara','Yemen','Zambia','Zimbabwe']


def date_joined(username):
    my_url = 'https://www.inaturalist.org/people/' + username
    
    #opening a connection and grabbing a page
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    #html parsing
    page_soup = soup(page_html, "html.parser")

    #focusing on just outputting a string of the date joined, and removing linebreaks
    date_joined_text = page_soup.find("span",{"class":"date"}).get_text().replace('\n', '')

    #converting output from (for example): "Joined: Nov 04, 2018" to "November 04 2018", comma removed so it doesn't interfer with csv writing
    date__stripped = date_joined_text[8:].replace(",", "")
    for key in full_months:
        if key in date__stripped:
            date_cleaned = date__stripped.replace(key, full_months[key])

    return date_cleaned

username_not_taken = []

f = open('Usernames_DateJoined.csv','w')
## Python will convert \n to os.linesep
f.write("Username," + "Date Joined \n")


for i in list_of_usernames:
    print(i)
    my_url = 'https://www.inaturalist.org/people/' + i
    try: 
        uClient = uReq(my_url)
    except:
        print("Username does not exist")
        username_not_taken.append(i)
        continue
    print(date_joined(i))
    f.write(i + ",")
    f.write(date_joined(i) + "\n")

for i in username_not_taken:
    f.write(i + ",Not Taken\n")

f.close()