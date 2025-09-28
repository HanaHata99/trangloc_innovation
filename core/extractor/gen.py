import csv, string


# Danh sách 200 mục A (125 câu + 75 câu ca dao tục ngữ)

phrases = [

    # --- 125 câu ban đầu ---
    "ăn cháo đá bát", "tre già măng mọc", "nồi đồng cối đá", "nước chảy đá mòn",
    "cá không ăn muối cá ươn", "mẹ tròn con vuông", "bánh chưng", "bánh tét",
    "áo dài", "nón lá", "công cha như núi Thái Sơn", "gánh nặng ân tình",
    "uống nước nhớ nguồn", "lá lành đùm lá rách", "chị ngã em nâng", "một con ngựa đau cả tàu bỏ cỏ",
    "khôn ngoan đối đáp người ngoài", "gừng càng già càng cay", "đói cho sạch rách cho thơm",
    "yêu cho roi cho vọt", "trăm nghe không bằng một thấy", "của một đồng công một nén",
    "đèn nhà ai nhà nấy rạng", "ăn quả nhớ kẻ trồng cây", "cha mẹ sinh con trời sinh tính",
    "bánh đa", "bánh cuốn", "bánh xèo", "bún bò Huế", "phở", "chả giò", "chè trôi nước",
    "mắm tôm", "xôi gấc", "chè lam", "cây tre Việt Nam", "trầu cau", "áo tứ thân", "khố",
    "nhạc cụ dân tộc", "đàn bầu", "đàn tranh", "đàn nguyệt", "sáo trúc", "trống đồng",
    "gánh hàng rong", "chợ quê", "ngày giỗ tổ Hùng Vương", "Tết Nguyên Đán", "Tết Trung Thu",
    "Tết Đoan Ngọ", "Hội Lim", "chèo", "tuồng", "cải lương", "dân ca quan họ", "hát xoan",
    "hát ví dặm", "hát then", "lễ hội đâm trâu", "lễ hội chọi trâu", "lễ hội Cầu Ngư",
    "tục xông đất", "tục lì xì", "tục gói bánh chưng ngày Tết", "tục dựng cây nêu",
    "tục thờ cúng tổ tiên", "lễ Vu Lan", "tảo mộ", "lễ cưới hỏi truyền thống", "áo dài cưới",
    "mâm quả cưới", "khăn đóng", "sính lễ", "trầu cau cưới", "tục lệ ăn hỏi", "tục nộp cheo",
    "tục mừng tuổi", "tục chúc Tết", "tục kiêng kỵ ngày Tết", "bánh in", "bánh tổ",
    "bánh khảo", "bánh phu thê", "bánh gai", "bánh ít lá gai", "bánh ít trần", "bánh dày",
    "bánh bột lọc", "bánh khoai mì", "cây mai vàng", "cây đào", "cây quất", "câu đối đỏ",
    "phong bao lì xì", "mâm ngũ quả", "lễ vật", "nhang đèn", "bàn thờ gia tiên",
    "lễ nhập trạch", "lễ đầy tháng", "lễ thôi nôi", "lễ tết đoan ngọ", "lễ mừng thọ",
    "lễ lên đồng", "nghi lễ hầu bóng", "lễ cúng giao thừa", "lễ cầu an", "lễ cầu mưa",
    "lễ cúng rằm tháng bảy", "lễ cúng ông Công ông Táo", "lễ hội chùa Hương", "lễ hội Yên Tử",
    "lễ hội đền Hùng", "tục nhuộm răng đen", "tục búi tóc", "tục xăm mình", "tục ăn trầu",
    "tục thờ mẫu", "tục thờ thần tài", "tục dựng vợ gả chồng", "tục thách cưới", "tục bắt vợ",
    "tục giã gạo", "tục làm bánh chưng bánh tét",

    # --- 75 câu ca dao tục ngữ ---
    "Tốt gỗ hơn tốt nước sơn", "Một cây làm chẳng nên non", "Ba cây chụm lại nên hòn núi cao",
    "Gần mực thì đen, gần đèn thì sáng", "Không thầy đố mày làm nên",
    "Có công mài sắt, có ngày nên kim", "Học ăn, học nói, học gói, học mở",
    "Tiên học lễ, hậu học văn", "Ăn vóc học hay", "Lời nói chẳng mất tiền mua, lựa lời mà nói cho vừa lòng nhau",
    "Ăn cơm mới, nói chuyện cũ", "Chết vinh còn hơn sống nhục", "Một giọt máu đào hơn ao nước lã",
    "Cháu ngoan thì ông bà thương", "Con hư tại mẹ, cháu hư tại bà", "Con hơn cha là nhà có phúc",
    "Giặc đến nhà, đàn bà cũng đánh", "Ăn cây nào rào cây ấy", "Ở hiền gặp lành", "Ác giả ác báo",
    "Nhân nào quả nấy", "Khôn ngoan chẳng lại thật thà", "Im lặng là vàng",
    "Thua keo này bày keo khác", "Cái nết đánh chết cái đẹp", "Của bền tại người",
    "Một miếng khi đói bằng một gói khi no", "Lá rụng về cội", "Có mới nới cũ",
    "Lửa thử vàng, gian nan thử sức", "Thương người như thể thương thân",
    "Trâu buộc ghét trâu ăn", "Thùng rỗng kêu to", "Biết thì thưa thốt, không biết thì dựa cột mà nghe",
    "Đi một ngày đàng học một sàng khôn", "Chớ thấy sóng cả mà ngã tay chèo",
    "Tránh vỏ dưa gặp vỏ dừa", "Thẳng như ruột ngựa", "Khéo ăn thì no, khéo co thì ấm",
    "Nói như rồng leo, làm như mèo mửa", "Cha nào con nấy", "Lúa tốt nhờ phân, người tốt nhờ khen",
    "Muốn ăn phải lăn vào bếp", "Một lần ngã là một lần bớt dại",
    "Thương cho roi cho vọt, ghét cho ngọt cho bùi", "Ăn ốc nói mò", "Ăn no vác nặng",
    "Đi đâu mà vội mà vàng", "Được làm vua thua làm giặc", "Đèn nhà ai nhà nấy rạng",
    "Cái khó ló cái khôn", "Lời chào cao hơn mâm cỗ", "Cơm không ăn gạo còn đó", "Dốt đặc cán mai",
    "Một điều nhịn, chín điều lành", "Cẩn tắc vô áy náy", "Chữ tín quý hơn vàng", "Có chí thì nên",
    "Trời không phụ lòng người", "Người ta là hoa đất", "Còn nước còn tát",
    "Không vào hang cọp sao bắt được cọp con", "Gió tầng nào gặp mây tầng ấy",
    "Đồng vợ đồng chồng tát biển Đông cũng cạn", "Vàng thật không sợ lửa",
    "Một lần bị rắn cắn, mười năm sợ dây thừng", "Kính lão đắc thọ", "Kính trên nhường dưới",
    "Giấy rách phải giữ lấy lề", "Cái gì không mua được bằng tiền thì mua được bằng nhiều tiền hơn",
    "Có thực mới vực được đạo", "Mèo mù vớ cá rán", "Gậy ông đập lưng ông",
    "Được đằng chân lân đằng đầu", "Vỏ quýt dày có móng tay nhọn"
]



# Mẫu câu

patterns = [
    "Tôi không hiểu câu {}",
    "Câu {} nghĩa là gì",
    "Bạn hiểu câu {} không",
    "Câu {} khó hiểu quá",
    "{} nghĩa là gì nhỉ",
    "Hãy giải thích câu {}",
    "Hãy giải thích {}",
    "Giải thích {} cho tôi",
    "Câu {} đúng là chí lý!",
    "Tôi thấy bạn là người {} thật đấy",
    "Bạn đúng là kiểu người {} rồi.",
    "Chơi với bạn lâu mới thấy bạn rất {}",
    "Bạn cứ như người {} trong truyền thuyết vậy.",
    "Mình cảm giác bạn đúng chất {} luôn.",
    "Càng tiếp xúc càng thấy bạn là người {}",
    "Nói thật, tôi luôn nghĩ bạn thuộc kiểu người {}",
    "Bạn làm tôi liên tưởng đến kiểu người {}",
    "Chẳng hiểu sao tôi cứ thấy bạn có chút gì đó {}",
    "Bạn đúng là mẫu người {} mà tôi thích.",
    "Có ai bảo bạn rất {} chưa nhỉ?",
    "Bạn thật sự toát lên vẻ {}",
    "Thật lòng đấy, tôi thấy bạn đúng là người {}",
    "Lần đầu gặp đã thấy bạn có nét {} rồi.",
    "Trong mắt tôi, bạn luôn là kiểu người {} đấy.",
]

bio_patterns = []

for pattern in patterns:
    strs = pattern.split()
    for i in range(len(strs)):
        if "{}" != strs[i]:
            strs[i] = "O"
    bio_pattern = " ".join(strs)
    bio_patterns.append(bio_pattern)

# Chức năng để tạo BIO tag cho mỗi câu
def generate_bio_tags(phrase):
    # Tạo BIO tags cho câu
    words = phrase.split()
    bio_tags = []
    for i in range(len(words)):
        if 0 == i:
            bio_tags.append('B-XXX')
        else:
            bio_tags.append('I-XXX')
    return " ".join(bio_tags)

def remove_punctuation(text):
    # Tạo một bảng tra cứu để loại bỏ tất cả dấu câu
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation))

# Tạo câu hỏi và BIO tags
sentences = []
for i, phrase in enumerate(phrases):
    for idx in range(len(patterns)):
        tmp_phrase = remove_punctuation(phrase)
        question = patterns[idx].lower().format(tmp_phrase)
        question = remove_punctuation(question)
        bio_tags = bio_patterns[idx].format(generate_bio_tags(tmp_phrase))
        sentences.append([question, bio_tags])

# Ghi vào file CSV
with open('train_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Câu hỏi", "BIO"])
    writer.writerows(sentences)

print("Đã tạo file CSV thành công!")

