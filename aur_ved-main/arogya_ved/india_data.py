# All India States and Major Cities with coordinates
INDIA_STATES = {
    "Andhra Pradesh": ["Visakhapatnam","Vijayawada","Guntur","Nellore","Kurnool","Kadapa","Tirupati","Rajahmundry","Kakinada","Eluru","Ongole","Anantapur","Vizianagaram","Chittoor","Srikakulam"],
    "Arunachal Pradesh": ["Itanagar","Naharlagun","Pasighat","Ziro","Bomdila","Tawang","Along","Tezu","Roing","Namsai"],
    "Assam": ["Guwahati","Silchar","Dibrugarh","Jorhat","Nagaon","Tinsukia","Tezpur","Bongaigaon","Karimganj","Sivasagar","Goalpara","Barpeta","Dhubri","Kokrajhar","North Lakhimpur"],
    "Bihar": ["Patna","Gaya","Bhagalpur","Muzaffarpur","Darbhanga","Arrah","Begusarai","Chhapra","Katihar","Munger","Purnia","Saharsa","Hajipur","Biharsharif","Siwan"],
    "Chhattisgarh": ["Raipur","Bhilai","Bilaspur","Korba","Durg","Rajnandgaon","Jagdalpur","Raigarh","Ambikapur","Dhamtari","Kawardha","Mahasamund","Kondagaon","Bastar","Janjgir"],
    "Goa": ["Panaji","Margao","Vasco da Gama","Mapusa","Ponda","Bicholim","Curchorem","Sanquelim","Canacona","Pernem"],
    "Gujarat": ["Ahmedabad","Surat","Vadodara","Rajkot","Bhavnagar","Jamnagar","Junagadh","Gandhinagar","Anand","Navsari","Morbi","Nadiad","Surendranagar","Bharuch","Mehsana","Porbandar","Amreli"],
    "Haryana": ["Faridabad","Gurugram","Panipat","Ambala","Yamunanagar","Rohtak","Hisar","Karnal","Sonipat","Panchkula","Bhiwani","Bahadurgarh","Jind","Sirsa","Fatehabad","Rewari"],
    "Himachal Pradesh": ["Shimla","Dharamshala","Solan","Mandi","Baddi","Kullu","Kangra","Una","Hamirpur","Chamba","Bilaspur","Nahan","Paonta Sahib","Sundernagar"],
    "Jharkhand": ["Ranchi","Jamshedpur","Dhanbad","Bokaro","Deoghar","Hazaribagh","Giridih","Ramgarh","Medininagar","Chaibasa","Dumka","Phusro","Sahibganj","Lohardaga"],
    "Karnataka": ["Bengaluru","Mysuru","Hubballi","Mangaluru","Belagavi","Kalaburagi","Ballari","Vijayapura","Shimoga","Tumkur","Davanagere","Bidar","Udupi","Hassan","Dharwad","Gadag","Raichur","Bagalkot"],
    "Kerala": ["Thiruvananthapuram","Kochi","Kozhikode","Thrissur","Kollam","Palakkad","Alappuzha","Kannur","Kottayam","Malappuram","Kasaragod","Punalur","Varkala","Kayamkulam"],
    "Madhya Pradesh": ["Bhopal","Indore","Jabalpur","Gwalior","Ujjain","Sagar","Dewas","Satna","Ratlam","Rewa","Murwara","Singrauli","Burhanpur","Khandwa","Bhind","Chhindwara","Guna","Shivpuri"],
    "Maharashtra": ["Mumbai","Pune","Nagpur","Thane","Nashik","Aurangabad","Solapur","Amravati","Kolhapur","Sangli","Malegaon","Jalgaon","Akola","Latur","Dhule","Nanded","Osmanabad","Parbhani","Jalna","Chandrapur"],
    "Manipur": ["Imphal","Thoubal","Bishnupur","Churachandpur","Kakching","Ukhrul","Senapati","Tamenglong","Jiribam"],
    "Meghalaya": ["Shillong","Tura","Jowai","Nongstoin","Baghmara","Resubelpara","Williamnagar","Ampati","Mairang"],
    "Mizoram": ["Aizawl","Lunglei","Saiha","Champhai","Kolasib","Serchhip","Lawngtlai","Mamit","Khawzawl"],
    "Nagaland": ["Kohima","Dimapur","Mokokchung","Tuensang","Wokha","Zunheboto","Phek","Mon","Longleng","Kiphire"],
    "Odisha": ["Bhubaneswar","Cuttack","Rourkela","Brahmapur","Sambalpur","Puri","Balasore","Bhadrak","Baripada","Jharsuguda","Jeypore","Bargarh","Kendrapara","Dhenkanal","Angul","Koraput","Rayagada"],
    "Punjab": ["Ludhiana","Amritsar","Jalandhar","Patiala","Bathinda","Mohali","Hoshiarpur","Batala","Pathankot","Moga","Abohar","Malerkotla","Khanna","Phagwara","Muktsar","Barnala"],
    "Rajasthan": ["Jaipur","Jodhpur","Kota","Bikaner","Ajmer","Udaipur","Bhilwara","Alwar","Bharatpur","Pali","Sikar","Sri Ganganagar","Barmer","Tonk","Chittorgarh","Nagaur","Sawai Madhopur"],
    "Sikkim": ["Gangtok","Namchi","Gyalshing","Mangan","Rangpo","Singtam","Jorethang","Nayabazar"],
    "Tamil Nadu": ["Chennai","Coimbatore","Madurai","Tiruchirappalli","Salem","Tirunelveli","Tiruppur","Vellore","Erode","Thoothukkudi","Dindigul","Thanjavur","Ranipet","Sivakasi","Karur","Hosur","Nagercoil","Kanchipuram","Cuddalore","Kumbakonam"],
    "Telangana": ["Hyderabad","Warangal","Nizamabad","Karimnagar","Ramagundam","Khammam","Mahbubnagar","Nalgonda","Adilabad","Suryapet","Miryalaguda","Siddipet","Mancherial","Hanamkonda","Zahirabad","Bodhan","Jagtial"],
    "Tripura": ["Agartala","Udaipur","Dharmanagar","Kailasahar","Ambassa","Belonia","Bishalgarh","Sabroom","Khowai","Sonamura"],
    "Uttar Pradesh": ["Lucknow","Kanpur","Ghaziabad","Agra","Meerut","Varanasi","Allahabad","Bareilly","Aligarh","Moradabad","Saharanpur","Gorakhpur","Noida","Firozabad","Muzaffarnagar","Mathura","Rampur","Shahjahanpur","Hapur","Ayodhya","Jhansi","Bahraich","Bulandshahr"],
    "Uttarakhand": ["Dehradun","Haridwar","Roorkee","Haldwani","Rudrapur","Kashipur","Rishikesh","Kotdwar","Ramnagar","Pithoragarh","Almora","Nainital","Mussoorie","Bageshwar"],
    "West Bengal": ["Kolkata","Asansol","Siliguri","Durgapur","Bardhaman","Malda","Baharampur","Habra","Kharagpur","Shantipur","Dankuni","Dhulian","Raiganj","Balurghat","Bangaon","Midnapore","Haldia","Cooch Behar","Jalpaiguri"],
    "Andaman and Nicobar Islands": ["Port Blair","Diglipur","Car Nicobar","Rangat","Mayabunder","Havelock","Neil Island"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman","Silvassa","Diu","Dadra"],
    "Delhi": ["New Delhi","Central Delhi","North Delhi","South Delhi","East Delhi","West Delhi","Dwarka","Rohini","Pitampura","Janakpuri","Laxmi Nagar"],
    "Jammu and Kashmir": ["Srinagar","Jammu","Anantnag","Baramulla","Sopore","Udhampur","Kathua","Poonch","Rajouri","Pulwama","Kupwara","Ganderbal","Bandipora","Kulgam"],
    "Ladakh": ["Leh","Kargil","Diskit","Padum","Nubra","Zanskar"],
    "Lakshadweep": ["Kavaratti","Agatti","Amini","Andrott","Minicoy"],
    "Puducherry": ["Puducherry","Karaikal","Mahe","Yanam","Oulgaret"]
}

# PHC locations across all India states for the map
INDIA_PHC_LOCATIONS = [
    # Telangana
    {"name":"PHC Hanamkonda","district":"Warangal","state":"Telangana","lat":18.0007,"lng":79.5941,"health_score":82,"doctors":3,"beds":30,"available_beds":12,"medicine_stock":75},
    {"name":"PHC Kazipet","district":"Warangal","state":"Telangana","lat":17.9784,"lng":79.5142,"health_score":58,"doctors":2,"beds":20,"available_beds":5,"medicine_stock":45},
    {"name":"CHC Warangal Urban","district":"Warangal","state":"Telangana","lat":17.9784,"lng":79.5941,"health_score":91,"doctors":8,"beds":80,"available_beds":35,"medicine_stock":88},
    {"name":"PHC Narsampet","district":"Warangal","state":"Telangana","lat":17.926,"lng":79.894,"health_score":42,"doctors":2,"beds":15,"available_beds":3,"medicine_stock":38},
    {"name":"PHC Karimnagar","district":"Karimnagar","state":"Telangana","lat":18.4386,"lng":79.1288,"health_score":76,"doctors":4,"beds":40,"available_beds":18,"medicine_stock":70},
    {"name":"PHC Nizamabad","district":"Nizamabad","state":"Telangana","lat":18.6725,"lng":78.0941,"health_score":68,"doctors":3,"beds":30,"available_beds":10,"medicine_stock":55},
    # Andhra Pradesh
    {"name":"PHC Vijayawada","district":"Krishna","state":"Andhra Pradesh","lat":16.5062,"lng":80.648,"health_score":84,"doctors":5,"beds":50,"available_beds":22,"medicine_stock":80},
    {"name":"PHC Visakhapatnam","district":"Visakhapatnam","state":"Andhra Pradesh","lat":17.6868,"lng":83.2185,"health_score":78,"doctors":4,"beds":40,"available_beds":15,"medicine_stock":72},
    {"name":"PHC Nellore","district":"Nellore","state":"Andhra Pradesh","lat":14.4426,"lng":79.9865,"health_score":65,"doctors":3,"beds":25,"available_beds":8,"medicine_stock":60},
    {"name":"PHC Tirupati","district":"Chittoor","state":"Andhra Pradesh","lat":13.6288,"lng":79.4192,"health_score":88,"doctors":6,"beds":60,"available_beds":28,"medicine_stock":85},
    # Tamil Nadu
    {"name":"PHC Chennai North","district":"Chennai","state":"Tamil Nadu","lat":13.0827,"lng":80.2707,"health_score":90,"doctors":7,"beds":70,"available_beds":32,"medicine_stock":90},
    {"name":"PHC Coimbatore","district":"Coimbatore","state":"Tamil Nadu","lat":11.0168,"lng":76.9558,"health_score":82,"doctors":5,"beds":50,"available_beds":20,"medicine_stock":78},
    {"name":"PHC Madurai","district":"Madurai","state":"Tamil Nadu","lat":9.9252,"lng":78.1198,"health_score":75,"doctors":4,"beds":40,"available_beds":16,"medicine_stock":70},
    {"name":"PHC Salem","district":"Salem","state":"Tamil Nadu","lat":11.6643,"lng":78.146,"health_score":70,"doctors":3,"beds":30,"available_beds":12,"medicine_stock":65},
    # Karnataka
    {"name":"PHC Bengaluru Central","district":"Bengaluru Urban","state":"Karnataka","lat":12.9716,"lng":77.5946,"health_score":92,"doctors":8,"beds":80,"available_beds":38,"medicine_stock":92},
    {"name":"PHC Mysuru","district":"Mysuru","state":"Karnataka","lat":12.2958,"lng":76.6394,"health_score":80,"doctors":5,"beds":45,"available_beds":20,"medicine_stock":76},
    {"name":"PHC Hubballi","district":"Dharwad","state":"Karnataka","lat":15.3647,"lng":75.124,"health_score":72,"doctors":3,"beds":30,"available_beds":11,"medicine_stock":65},
    # Maharashtra
    {"name":"PHC Mumbai Suburban","district":"Mumbai","state":"Maharashtra","lat":19.076,"lng":72.8777,"health_score":88,"doctors":8,"beds":80,"available_beds":35,"medicine_stock":86},
    {"name":"PHC Pune","district":"Pune","state":"Maharashtra","lat":18.5204,"lng":73.8567,"health_score":85,"doctors":6,"beds":60,"available_beds":25,"medicine_stock":82},
    {"name":"PHC Nagpur","district":"Nagpur","state":"Maharashtra","lat":21.1458,"lng":79.0882,"health_score":78,"doctors":5,"beds":50,"available_beds":22,"medicine_stock":74},
    {"name":"PHC Nashik","district":"Nashik","state":"Maharashtra","lat":19.9975,"lng":73.7898,"health_score":70,"doctors":4,"beds":35,"available_beds":14,"medicine_stock":65},
    # Gujarat
    {"name":"PHC Ahmedabad","district":"Ahmedabad","state":"Gujarat","lat":23.0225,"lng":72.5714,"health_score":87,"doctors":7,"beds":70,"available_beds":30,"medicine_stock":84},
    {"name":"PHC Surat","district":"Surat","state":"Gujarat","lat":21.1702,"lng":72.8311,"health_score":83,"doctors":5,"beds":55,"available_beds":24,"medicine_stock":79},
    {"name":"PHC Vadodara","district":"Vadodara","state":"Gujarat","lat":22.3072,"lng":73.1812,"health_score":76,"doctors":4,"beds":40,"available_beds":17,"medicine_stock":72},
    # Rajasthan
    {"name":"PHC Jaipur","district":"Jaipur","state":"Rajasthan","lat":26.9124,"lng":75.7873,"health_score":81,"doctors":5,"beds":50,"available_beds":22,"medicine_stock":78},
    {"name":"PHC Jodhpur","district":"Jodhpur","state":"Rajasthan","lat":26.2389,"lng":73.0243,"health_score":72,"doctors":4,"beds":35,"available_beds":14,"medicine_stock":65},
    {"name":"PHC Udaipur","district":"Udaipur","state":"Rajasthan","lat":24.5854,"lng":73.7125,"health_score":77,"doctors":4,"beds":40,"available_beds":18,"medicine_stock":73},
    # Uttar Pradesh
    {"name":"PHC Lucknow","district":"Lucknow","state":"Uttar Pradesh","lat":26.8467,"lng":80.9462,"health_score":79,"doctors":5,"beds":50,"available_beds":20,"medicine_stock":75},
    {"name":"PHC Kanpur","district":"Kanpur","state":"Uttar Pradesh","lat":26.4499,"lng":80.3319,"health_score":68,"doctors":4,"beds":40,"available_beds":14,"medicine_stock":60},
    {"name":"PHC Agra","district":"Agra","state":"Uttar Pradesh","lat":27.1767,"lng":78.0081,"health_score":72,"doctors":4,"beds":35,"available_beds":15,"medicine_stock":66},
    {"name":"PHC Varanasi","district":"Varanasi","state":"Uttar Pradesh","lat":25.3176,"lng":82.9739,"health_score":74,"doctors":4,"beds":40,"available_beds":16,"medicine_stock":69},
    # Delhi
    {"name":"PHC New Delhi Central","district":"Central Delhi","state":"Delhi","lat":28.6139,"lng":77.209,"health_score":91,"doctors":9,"beds":90,"available_beds":42,"medicine_stock":90},
    {"name":"PHC South Delhi","district":"South Delhi","state":"Delhi","lat":28.5355,"lng":77.391,"health_score":88,"doctors":7,"beds":70,"available_beds":32,"medicine_stock":86},
    # West Bengal
    {"name":"PHC Kolkata North","district":"North 24 Parganas","state":"West Bengal","lat":22.5726,"lng":88.3639,"health_score":83,"doctors":6,"beds":60,"available_beds":26,"medicine_stock":80},
    {"name":"PHC Siliguri","district":"Darjeeling","state":"West Bengal","lat":26.7271,"lng":88.3953,"health_score":70,"doctors":3,"beds":30,"available_beds":12,"medicine_stock":64},
    # Punjab
    {"name":"PHC Amritsar","district":"Amritsar","state":"Punjab","lat":31.634,"lng":74.8723,"health_score":80,"doctors":5,"beds":45,"available_beds":19,"medicine_stock":76},
    {"name":"PHC Ludhiana","district":"Ludhiana","state":"Punjab","lat":30.901,"lng":75.8573,"health_score":78,"doctors":5,"beds":45,"available_beds":20,"medicine_stock":74},
    # Madhya Pradesh
    {"name":"PHC Bhopal","district":"Bhopal","state":"Madhya Pradesh","lat":23.2599,"lng":77.4126,"health_score":80,"doctors":5,"beds":50,"available_beds":22,"medicine_stock":76},
    {"name":"PHC Indore","district":"Indore","state":"Madhya Pradesh","lat":22.7196,"lng":75.8577,"health_score":84,"doctors":6,"beds":55,"available_beds":25,"medicine_stock":80},
    # Bihar
    {"name":"PHC Patna","district":"Patna","state":"Bihar","lat":25.5941,"lng":85.1376,"health_score":66,"doctors":4,"beds":40,"available_beds":14,"medicine_stock":58},
    {"name":"PHC Gaya","district":"Gaya","state":"Bihar","lat":24.7955,"lng":85.0002,"health_score":55,"doctors":3,"beds":25,"available_beds":8,"medicine_stock":48},
    # Odisha
    {"name":"PHC Bhubaneswar","district":"Khordha","state":"Odisha","lat":20.2961,"lng":85.8245,"health_score":79,"doctors":5,"beds":45,"available_beds":20,"medicine_stock":75},
    {"name":"PHC Cuttack","district":"Cuttack","state":"Odisha","lat":20.4625,"lng":85.8828,"health_score":73,"doctors":4,"beds":35,"available_beds":15,"medicine_stock":67},
    # Kerala
    {"name":"PHC Thiruvananthapuram","district":"Thiruvananthapuram","state":"Kerala","lat":8.5241,"lng":76.9366,"health_score":93,"doctors":8,"beds":75,"available_beds":38,"medicine_stock":92},
    {"name":"PHC Kochi","district":"Ernakulam","state":"Kerala","lat":9.9312,"lng":76.2673,"health_score":90,"doctors":7,"beds":65,"available_beds":30,"medicine_stock":89},
    # Jharkhand
    {"name":"PHC Ranchi","district":"Ranchi","state":"Jharkhand","lat":23.3441,"lng":85.3096,"health_score":68,"doctors":4,"beds":35,"available_beds":13,"medicine_stock":62},
    # Assam
    {"name":"PHC Guwahati","district":"Kamrup","state":"Assam","lat":26.1445,"lng":91.7362,"health_score":72,"doctors":4,"beds":38,"available_beds":16,"medicine_stock":66},
    # Himachal Pradesh
    {"name":"PHC Shimla","district":"Shimla","state":"Himachal Pradesh","lat":31.1048,"lng":77.1734,"health_score":82,"doctors":4,"beds":35,"available_beds":16,"medicine_stock":78},
    # Uttarakhand
    {"name":"PHC Dehradun","district":"Dehradun","state":"Uttarakhand","lat":30.3165,"lng":78.0322,"health_score":80,"doctors":4,"beds":40,"available_beds":18,"medicine_stock":75},
    # Haryana
    {"name":"PHC Gurugram","district":"Gurugram","state":"Haryana","lat":28.4595,"lng":77.0266,"health_score":86,"doctors":6,"beds":55,"available_beds":24,"medicine_stock":83},
    {"name":"PHC Faridabad","district":"Faridabad","state":"Haryana","lat":28.4089,"lng":77.3178,"health_score":79,"doctors":5,"beds":45,"available_beds":19,"medicine_stock":74},
    # Chhattisgarh
    {"name":"PHC Raipur","district":"Raipur","state":"Chhattisgarh","lat":21.2514,"lng":81.6296,"health_score":70,"doctors":4,"beds":38,"available_beds":15,"medicine_stock":64},
    # Goa
    {"name":"PHC Panaji","district":"North Goa","state":"Goa","lat":15.4909,"lng":73.8278,"health_score":88,"doctors":5,"beds":40,"available_beds":20,"medicine_stock":86},
    # Jammu & Kashmir
    {"name":"PHC Srinagar","district":"Srinagar","state":"Jammu and Kashmir","lat":34.0837,"lng":74.7973,"health_score":74,"doctors":4,"beds":38,"available_beds":16,"medicine_stock":68},
    {"name":"PHC Jammu","district":"Jammu","state":"Jammu and Kashmir","lat":32.7266,"lng":74.857,"health_score":76,"doctors":4,"beds":40,"available_beds":17,"medicine_stock":71},
    # Northeast
    {"name":"PHC Imphal","district":"Imphal West","state":"Manipur","lat":24.817,"lng":93.9368,"health_score":66,"doctors":3,"beds":28,"available_beds":11,"medicine_stock":60},
    {"name":"PHC Shillong","district":"East Khasi Hills","state":"Meghalaya","lat":25.5788,"lng":91.8933,"health_score":74,"doctors":4,"beds":35,"available_beds":15,"medicine_stock":68},
    {"name":"PHC Aizawl","district":"Aizawl","state":"Mizoram","lat":23.7271,"lng":92.7176,"health_score":72,"doctors":3,"beds":30,"available_beds":13,"medicine_stock":65},
    {"name":"PHC Kohima","district":"Kohima","state":"Nagaland","lat":25.6751,"lng":94.1086,"health_score":68,"doctors":3,"beds":25,"available_beds":10,"medicine_stock":62},
    {"name":"PHC Agartala","district":"West Tripura","state":"Tripura","lat":23.8315,"lng":91.2868,"health_score":70,"doctors":3,"beds":30,"available_beds":12,"medicine_stock":64},
    {"name":"PHC Itanagar","district":"Papum Pare","state":"Arunachal Pradesh","lat":27.0844,"lng":93.6053,"health_score":65,"doctors":3,"beds":25,"available_beds":10,"medicine_stock":60},
    {"name":"PHC Gangtok","district":"East Sikkim","state":"Sikkim","lat":27.3389,"lng":88.6065,"health_score":78,"doctors":3,"beds":28,"available_beds":13,"medicine_stock":74},
]
