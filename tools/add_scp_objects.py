from pathlib import Path
import json
import math
import random
import re
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "script.js"
CREDITS = ROOT / "credits.html"
PORTRAITS = ROOT / "assets" / "portraits"
DRAWINGS = ROOT / "assets" / "drawings"
SHAK = ROOT / "assets" / "drawings-shakalized"

for path in (PORTRAITS, DRAWINGS, SHAK):
    path.mkdir(parents=True, exist_ok=True)

ITEMS = [
    ("SCP-018", "Супермяч", ["18", "018", "scp018", "супермяч", "super ball"], "#d94b4b", "machine", "ball",
     "https://scp-wiki.wikidot.com/scp-018",
     ["Выглядит как обычный резиновый мяч Super Ball 1969 года.", "После начала движения отскакивает всё быстрее и опаснее.", "Может пробивать препятствия, когда набирает огромную скорость."],
     dict(objectClass="Euclid", anomalyType="предмет", form="артефакт", danger="высокий", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["пространство", "прикосновение"], activation="использование", location="усиленный контейнер", tags=["мяч", "отскок", "скорость"], document="Небольшой резиновый мяч после броска или падения начинает отскакивать с возрастающей скоростью и энергией, быстро превращаясь в разрушительный снаряд.", containment="Объект хранится в усиленном контейнере с амортизирующими слоями. Любое неконтролируемое движение запрещено.", emoji=["🏀", "↗️", "💥", "⚡", "🧱"], drawingHint="Маленький мяч с линиями траектории, трещины на стене и отметки ударов.")),
    ("SCP-127", "Живое оружие", ["127", "scp127", "живое оружие", "living gun"], "#8b2f35", "danger", "gun",
     "https://scp-wiki.wikidot.com/scp-127",
     ["Выглядит как органический пистолет с живыми тканями.", "Стреляет зубоподобными снарядами вместо обычных патронов.", "Периодически регенерирует боезапас внутри себя."],
     dict(objectClass="Safe", anomalyType="устройство", form="артефакт", danger="средний", sentience="неразумный", aggression="пассивный", living="живой", physical="физический", effects=["контакт"], activation="использование", location="оружейный сейф", tags=["оружие", "биология", "зубы"], document="Органическое огнестрельное оружие состоит из живой ткани и производит твердые зубоподобные снаряды, восстанавливая их без внешних боеприпасов.", containment="Объект хранится в оружейном сейфе. Испытания разрешены только на полигоне с медицинским наблюдением.", emoji=["🔫", "🫀", "🦷", "🧬", "🎯"], drawingHint="Пистолет с органическими прожилками, зубы-патроны и грубые красные мазки.")),
    ("SCP-207", "Кола", ["207", "scp207", "кола", "coca cola", "кока кола"], "#d43b32", "machine", "bottle",
     "https://scp-wiki.wikidot.com/scp-207",
     ["Это стеклянные бутылки газировки Coca-Cola.", "Выпивший получает ускорение и выносливость, но не может остановиться.", "Длительный эффект приводит к опасному истощению организма."],
     dict(objectClass="Safe", anomalyType="предмет", form="жидкость", danger="средний", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["контакт", "сознание"], activation="использование", location="медицинский сейф", tags=["газировка", "ускорение", "истощение"], document="Набор бутылок газированного напитка вызывает резкое повышение скорости, выносливости и двигательной активности у выпившего, постепенно перегружая тело.", containment="Бутылки хранятся в запертом холодильном контейнере. Употребление допускается только по разрешению медицинского персонала.", emoji=["🥤", "🏃", "⚡", "❤️", "☠️"], drawingHint="Бутылка колы, пузырьки, бегущий силуэт и предупреждающий медицинский знак.")),
    ("SCP-244", "Ледяной туман", ["244", "scp244", "ледяной туман", "ваза", "кувшин"], "#9ec7d6", "void", "vase",
     "https://scp-wiki.wikidot.com/scp-244",
     ["Это древние керамические сосуды, выделяющие холодный туман.", "Туман резко снижает температуру вокруг объекта.", "Опасность связана с замерзанием и расширением зоны холода."],
     dict(objectClass="Euclid", anomalyType="предмет", form="артефакт", danger="высокий", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["пространство", "контакт"], activation="случайная активация", location="термоизолированная камера", tags=["сосуд", "холод", "туман"], document="Керамический сосуд постоянно выделяет холодный туман, который снижает температуру и создает опасную зону обморожения вокруг объекта.", containment="Сосуд хранится в термоизолированной камере. Доступ разрешен только в защитном снаряжении и при контроле температуры.", emoji=["🏺", "🌫️", "❄️", "🥶", "🚪"], drawingHint="Кувшин с густым туманом, снежинки и промерзший пол вокруг.")),
    ("SCP-268", "Кепка невидимости", ["268", "scp268", "кепка", "кепка невидимости", "cap of neglect"], "#5b6b58", "watch", "cap",
     "https://scp-wiki.wikidot.com/scp-268",
     ["Выглядит как твидовая кепка.", "Надевшего перестают замечать окружающие.", "Эффект похож не на невидимость, а на игнорирование внимания."],
     dict(objectClass="Safe", anomalyType="предмет", form="артефакт", danger="низкий", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["зрение", "сознание", "память"], activation="использование", location="малый сейф", tags=["кепка", "незаметность", "внимание"], document="При ношении кепки наблюдатели перестают обращать внимание на владельца, даже если тот находится в поле зрения.", containment="Кепка хранится в малом сейфе. Испытания проводятся с наблюдением через журналирование и камеры.", emoji=["🧢", "👁️", "🚫", "🧠", "👤"], drawingHint="Кепка на голове человека, вокруг люди смотрят мимо и знаки игнорирования.")),
    ("SCP-1344", "Глаза истины", ["1344", "scp1344", "очки", "глаза истины", "glasses"], "#a2b4c8", "watch", "glasses",
     "https://scp-wiki.wikidot.com/scp-1344",
     ["Объект связан с очками, меняющими восприятие.", "Носитель видит скрытые или необычные сущности.", "Эффект может быть психологически опасным."],
     dict(objectClass="Euclid", anomalyType="предмет", form="устройство", danger="средний", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["зрение", "сознание"], activation="использование", location="оптический контейнер", tags=["очки", "зрение", "скрытое"], document="Аномальная оптика меняет визуальное восприятие пользователя и открывает детали, которые обычное зрение не фиксирует.", containment="Очки хранятся в непрозрачном футляре. Испытания требуют психологического наблюдения после использования.", emoji=["👓", "👁️", "👻", "🧠", "⚠️"], drawingHint="Очки, за линзами видны странные силуэты и испуганный наблюдатель.")),
    ("SCP-1509", "Кожа дракона", ["1509", "scp1509", "кожа дракона", "перчатки"], "#b6653b", "danger", "glove",
     "https://scp-wiki.wikidot.com/scp-1509",
     ["Объект выглядит как защитные перчатки или материал.", "Связан с экстремальной жарой и огнем.", "Использование дает опасный эффект вокруг владельца."],
     dict(objectClass="Euclid", anomalyType="предмет", form="артефакт", danger="высокий", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["прикосновение", "контакт"], activation="использование", location="огнестойкий контейнер", tags=["огонь", "перчатки", "жар"], document="Аномальный защитный материал связан с теплом и огнем: при использовании проявляет свойства, превышающие обычную термозащиту.", containment="Объект хранится в огнестойком контейнере. Испытания проводятся на пожарном полигоне с дистанционным наблюдением.", emoji=["🧤", "🔥", "🐉", "🌡️", "⚠️"], drawingHint="Грубая перчатка, языки пламени и знак высокой температуры.")),
    ("SCP-1576", "Предсмертные записи", ["1576", "scp1576", "предсмертные записи", "ноты", "музыка"], "#c9b47a", "void", "record",
     "https://scp-wiki.wikidot.com/scp-1576",
     ["Объект связан с музыкальными записями и сообщениями умерших.", "Записи позволяют услышать слова людей после смерти.", "Эффект проявляется через воспроизведение носителя."],
     dict(objectClass="Safe", anomalyType="предмет", form="документ", danger="низкий", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["слух", "память"], activation="использование", location="аудиоархив", tags=["запись", "смерть", "голос"], document="Аудионосители позволяют получить сообщения, связанные с умершими людьми, и воспринимаются как посмертная коммуникация.", containment="Носители хранятся в архиве аудиоматериалов. Прослушивание протоколируется и проводится в изолированной комнате.", emoji=["🎵", "💿", "💀", "📻", "🗣️"], drawingHint="Пластинка или кассета, ноты и маленький призрачный речевой пузырь.")),
    ("SCP-1853", "Производительность", ["1853", "scp1853", "производительность", "таблетки", "performance enhancer"], "#4f9a6c", "machine", "syringe",
     "https://scp-wiki.wikidot.com/scp-1853",
     ["Это вещество, повышающее эффективность действий человека.", "Пользователь быстрее анализирует угрозы и точнее действует.", "Побочные эффекты делают применение рискованным."],
     dict(objectClass="Safe", anomalyType="предмет", form="жидкость", danger="средний", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["сознание", "контакт"], activation="использование", location="медицинский сейф", tags=["стимулятор", "реакция", "эффективность"], document="Химическое вещество повышает скорость реакции, точность и способность быстро выбирать оптимальные действия, но перегружает организм.", containment="Ампулы хранятся в медицинском сейфе. Применение требует разрешения и последующего обследования.", emoji=["💉", "🎯", "🧠", "⚡", "⚠️"], drawingHint="Ампула со стимулятором, прицел и ускоренный силуэт человека.")),
    ("SCP-2176", "Призрачный свет", ["2176", "scp2176", "ghostlight", "призрачный свет", "лампы"], "#9fd0d7", "void", "lamp",
     "https://scp-wiki.wikidot.com/scp-2176",
     ["Это люминесцентные лампы, известные как Ghostlight.", "При разбитии они подавляют электронику и свет вокруг.", "Часто полезны против технологических угроз."],
     dict(objectClass="Thaumiel", anomalyType="предмет", form="устройство", danger="средний", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["свет", "пространство"], activation="физический контакт", location="хранилище спецсредств", tags=["лампа", "свет", "электроника"], document="Аномальные лампы при разрушении создают эффект подавления электрических и световых систем в области воздействия.", containment="Лампы хранятся в защищенных упаковках. Использование разрешено как спецсредство при технологических угрозах.", emoji=["💡", "👻", "⚡", "📵", "🔦"], drawingHint="Люминесцентная лампа, трещина, погасшие экраны и голубоватый свет.")),
]

EXTRA = [
    ("SCP-008", "Зомби-чумы", ["8", "008", "scp008", "зомби чума", "зомби-чумы"], "#6ea65f", "danger", "biohazard", "https://scp-wiki.wikidot.com/scp-008", ["Это сложный прион, вызывающий симптомы, похожие на зомби-инфекцию.", "Заражение приводит к агрессии, некрозу и потере высших функций.", "Содержится как биологическая угроза высокого уровня."], dict(objectClass="Euclid", anomalyType="вирус", form="жидкость", danger="критический", sentience="неразумный", aggression="агрессивный", living="живой", physical="физический", effects=["контакт", "сознание"], activation="физический контакт", location="биолаборатория", tags=["прион", "заражение", "зомби"], document="Аномальный прион вызывает у зараженных тяжелые физиологические изменения, агрессию и поведение, напоминающее классические зомби-сценарии.", containment="Образцы хранятся в герметичной биолаборатории. Все контакты требуют полной биозащиты и карантина.", emoji=["🧫", "🧟", "☣️", "🩸", "🔒"], drawingHint="Пробирка с биоопасным знаком, силуэт зараженного и капли жидкости.")),
    ("SCP-012", "Плохая композиция", ["12", "012", "scp012", "плохая композиция", "ноты"], "#7a2d2d", "void", "sheet", "https://scp-wiki.wikidot.com/scp-012", ["Это незавершенная музыкальная партитура, написанная кровью.", "Люди рядом пытаются закончить произведение собственной кровью.", "Воздействие связано с чтением и навязчивым поведением."], dict(objectClass="Euclid", anomalyType="документ", form="текст", danger="высокий", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["чтение", "сознание"], activation="чтение", location="запечатанный архив", tags=["партитура", "кровь", "навязчивость"], document="Незавершенная музыкальная партитура вызывает у наблюдателей непреодолимое желание дописать ее, используя собственную кровь.", containment="Документ хранится в закрытом контейнере. Просмотр без письменного разрешения запрещен.", emoji=["🎼", "🩸", "✍️", "🧠", "🚫"], drawingHint="Лист нот с красными пятнами и рука, тянущаяся к партитуре.")),
    ("SCP-023", "Черный пес-призрак", ["23", "023", "scp023", "черный пес", "black shuck"], "#252525", "danger", "dog", "https://scp-wiki.wikidot.com/scp-023", ["Выглядит как крупная черная собака с огненными глазами.", "Встреча с объектом связана с последующей смертью близких.", "Объект проявляет свойства фольклорного призрачного пса."], dict(objectClass="Euclid", anomalyType="существо", form="животное", danger="высокий", sentience="неизвестно", aggression="реагирует при условии", living="живой", physical="физический", effects=["зрение", "память"], activation="взгляд", location="изолированный вольер", tags=["пес", "огонь", "смерть"], document="Крупная черная собака с горящими глазами вызывает цепочку смертельных событий, связанных с людьми, увидевшими объект.", containment="Объект содержится в изолированном вольере с ограничением визуального контакта.", emoji=["🐕", "🔥", "👁️", "💀", "🌑"], drawingHint="Черный пес с горящими глазами, следы лап и знак смерти.")),
    ("SCP-076", "Авель", ["76", "076", "scp076", "авель", "able"], "#8a3838", "danger", "warrior", "https://scp-wiki.wikidot.com/scp-076", ["Состоит из каменного саркофага и враждебного гуманоидного субъекта.", "Субъект крайне опасен в ближнем бою и возвращается после смерти.", "Связан с именем Авель."], dict(objectClass="Keter", anomalyType="существо", form="гуманоид", danger="критический", sentience="разумный", aggression="агрессивный", living="живой", physical="физический", effects=["контакт"], activation="случайная активация", location="усиленная камера", tags=["саркофаг", "воин", "возрождение"], document="Комплекс включает саркофаг и гуманоидного субъекта, который периодически выходит из него и проявляет крайне высокий уровень боевой опасности.", containment="Саркофаг содержится в усиленной камере. При появлении субъекта активируются летальные протоколы подавления.", emoji=["⚰️", "⚔️", "🧍", "💀", "🔒"], drawingHint="Саркофаг, вооруженный гуманоид и следы боя.")),
    ("SCP-093", "Красный морской объект", ["93", "093", "scp093", "красный диск", "red sea object"], "#b72d2d", "void", "disc", "https://scp-wiki.wikidot.com/scp-093", ["Это красный диск, связанный с зеркалами.", "При контакте с зеркалом открывает путь в другое место.", "Исследования связаны с пустынным альтернативным миром и гигантскими фигурами."], dict(objectClass="Euclid", anomalyType="предмет", form="артефакт", danger="средний", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["пространство", "зрение"], activation="использование", location="зеркальная тестовая камера", tags=["диск", "зеркало", "другой мир"], document="Красный дискообразный объект при использовании с зеркальными поверхностями открывает проходы в альтернативную среду.", containment="Объект хранится отдельно от зеркал. Тесты проводятся только в подготовленной камере с аварийным извлечением.", emoji=["🔴", "🪞", "🚪", "🏜️", "👁️"], drawingHint="Красный диск перед зеркалом, проход и пустынный силуэт за стеклом.")),
    ("SCP-1981", "Рональд Рейган говорит", ["1981", "scp1981", "рональд рейган", "reagan cut up"], "#4d5a7c", "void", "tv", "https://scp-wiki.wikidot.com/scp-1981", ["Это видеозапись речи Рональда Рейгана.", "При каждом просмотре речь и повреждения на теле меняются.", "Запись становится все более тревожной и невозможной."], dict(objectClass="Safe", anomalyType="документ", form="текст", danger="средний", sentience="неразумный", aggression="пассивный", living="неживой", physical="физический", effects=["зрение", "слух", "сознание"], activation="использование", location="видеоархив", tags=["видеокассета", "речь", "изменение"], document="Видеозапись публичной речи изменяется при каждом просмотре, демонстрируя невозможные отклонения в содержании и состоянии выступающего.", containment="Копии записи хранятся в видеоархиве. Просмотр допускается только в исследовательских целях.", emoji=["📼", "🎙️", "🇺🇸", "🩸", "📺"], drawingHint="Старый телевизор с политиком на экране, помехи и красные царапины.")),
    ("SCP-2295", "Медвежонок-заплатка", ["2295", "scp2295", "медвежонок заплатка", "bear with a heart"], "#b78d6a", "watch", "patchbear", "https://scp-wiki.wikidot.com/scp-2295", ["Это плюшевый медведь из лоскутов ткани.", "Он создает тканевые органы для лечения повреждений.", "Обычно проявляет заботливое поведение рядом с раненым человеком."], dict(objectClass="Safe", anomalyType="существо", form="артефакт", danger="низкий", sentience="разумный", aggression="пассивный", living="живой", physical="физический", effects=["контакт"], activation="приближение", location="медицинское крыло", tags=["медведь", "лечение", "сердце"], document="Плюшевый медведь способен создавать тканевые аналоги органов и использовать их для помощи пациентам с тяжелыми повреждениями.", containment="Объект содержится в медицинском крыле и допускается к пациентам только под наблюдением врачей.", emoji=["🧸", "❤️", "🪡", "🏥", "✅"], drawingHint="Лоскутный медвежонок с сердцем, игла и пациент на койке.")),
    ("SCP-2662", "Ктулху-подросток", ["2662", "scp2662", "ктулху", "ктулху подросток"], "#596f6a", "void", "tentacle", "https://scp-wiki.wikidot.com/scp-2662", ["Это огромный гуманоид с щупальцами, похожий на мифического древнего бога.", "Он не хочет культов, но люди всё равно создают их вокруг него.", "Объект обычно выглядит скорее раздраженным, чем злонамеренным."], dict(objectClass="Keter", anomalyType="существо", form="гуманоид", danger="высокий", sentience="разумный", aggression="пассивный", living="живой", physical="физический", effects=["сознание", "разговор"], activation="приближение", location="гуманоидная камера", tags=["щупальца", "культ", "древний бог"], document="Крупный гуманоидный субъект с щупальцами непроизвольно провоцирует культовую активность и навязчивое поклонение среди людей.", containment="Объект содержится в гуманоидной камере. Контакт с внешними группами и культовыми материалами запрещен.", emoji=["🐙", "🧍", "🕯️", "😑", "🧠"], drawingHint="Большой гуманоид с щупальцами, свечи культа и недовольное лицо.")),
    ("SCP-303", "Дверной человек", ["303", "scp303", "дверной человек", "the doorman"], "#4d3a32", "void", "door", "https://scp-wiki.wikidot.com/scp-303", ["Объект появляется за дверью, когда человек пытается ее открыть.", "Наблюдатель испытывает сильный страх и не может войти.", "Чаще всего видны только глаза и часть лица в темноте."], dict(objectClass="Euclid", anomalyType="существо", form="гуманоид", danger="средний", sentience="разумный", aggression="реагирует при условии", living="живой", physical="нефизический", effects=["зрение", "сознание"], activation="приближение", location="переходы и двери", tags=["дверь", "страх", "глаза"], document="Аномальная фигура проявляется за дверями и вызывает у людей сильную реакцию страха, препятствующую проходу.", containment="Персонал обязан сообщать о проявлениях у дверей. Зоны с повторными событиями изолируются.", emoji=["🚪", "👁️", "😨", "🌑", "🚫"], drawingHint="Приоткрытая дверь, темное лицо с глазами и испуганная рука на ручке.")),
    ("SCP-3199", "Люди не были людьми", ["3199", "scp3199", "люди не были людьми", "курица", "humans refuted"], "#d2c7a2", "danger", "birdman", "https://scp-wiki.wikidot.com/scp-3199", ["Это агрессивные бледные гуманоидные существа с птичьими чертами.", "Они быстро размножаются яйцами.", "Содержание осложняется скоростью, силой и количеством потомства."], dict(objectClass="Keter", anomalyType="существо", form="животное", danger="критический", sentience="неизвестно", aggression="агрессивный", living="живой", physical="физический", effects=["контакт"], activation="приближение", location="биологический вольер", tags=["яйца", "птица", "размножение"], document="Бледные гуманоидные организмы с птичьими признаками проявляют агрессию и способны быстро увеличивать численность через аномальные яйца.", containment="Объекты содержатся в укрепленном биологическом вольере. Яйца немедленно изымаются и уничтожаются по протоколу.", emoji=["🥚", "🐔", "🧍", "💢", "☣️"], drawingHint="Бледное птицеподобное существо, яйца и следы когтей.")),
]

ITEMS += EXTRA

def js_literal(value):
    text = json.dumps(value, ensure_ascii=False, indent=2)
    for key in ["id", "title", "icon", "label", "kind", "color", "aliases", "source", "hints", "objectClass", "anomalyType", "form", "danger", "sentience", "aggression", "living", "physical", "effects", "activation", "location", "tags", "document", "containment", "emoji", "drawingHint"]:
        text = text.replace(f'"{key}":', f"{key}:")
    return text

def update_script():
    script = SCRIPT.read_text(encoding="utf-8")
    obj_chunks, data_chunks = [], []
    for id_, title, aliases, color, kind, art, source, hints, data in ITEMS:
        if f'id: "{id_}"' in script or f'"{id_}":' in script:
            continue
        obj = dict(id=id_, title=title, icon=dict(label=id_.split("-")[1], kind=kind, color=color), aliases=aliases, source=source, hints=hints)
        obj_chunks.append("  " + js_literal(obj).replace("\n", "\n  "))
        data_chunks.append(f'  "{id_}": ' + js_literal(data).replace("\n", "\n  "))

    if obj_chunks:
        marker = "\n];\n\nconst challengeData = {"
        script = script.replace(marker, ",\n" + ",\n".join(obj_chunks) + "\n" + marker, 1)
        marker = "\n};\n\nconst levelTypes = ["
        script = script.replace(marker, ",\n" + ",\n".join(data_chunks) + "\n" + marker, 1)
        SCRIPT.write_text(script, encoding="utf-8")
    return len(obj_chunks)

W = H = 1024
BLACK = (5, 5, 5)
WHITE = (255, 255, 255)
RED = (215, 35, 35)
BLUE = (45, 110, 210)
GRAY = (120, 120, 120)

def symbol(draw, art, color, sketch=False):
    w = 5 if sketch else 11
    c = BLACK if sketch else color
    def line(points, col=None, width=None): draw.line(points, fill=col or c, width=width or w, joint="curve")
    def ell(box, outline=None, fill=None, width=None): draw.ellipse(box, outline=outline or c, fill=fill, width=width or w)
    def rect(box, outline=None, fill=None, width=None): draw.rectangle(box, outline=outline or c, fill=fill, width=width or w)
    def poly(points, outline=None, fill=None, width=None):
        if fill: draw.polygon(points, fill=fill)
        draw.line(points + [points[0]], fill=outline or c, width=width or w, joint="curve")

    if art == "ball":
        ell((330,330,690,690), fill=None if sketch else (220,70,70)); line([(210,700),(330,590),(230,500)], GRAY); line([(690,330),(800,220),(760,370)], GRAY)
    elif art == "gun":
        poly([(210,430),(620,360),(730,430),(520,500),(500,670),(390,670),(410,525),(230,520)], fill=None if sketch else (80,35,35)); line([(300,455),(600,405)], RED); ell((570,440,630,500))
    elif art == "bottle":
        rect((420,180,590,780), fill=None if sketch else (180,40,40)); rect((455,120,555,190), fill=None if sketch else (210,210,210)); rect((440,390,570,560), fill=None if sketch else WHITE); line([(470,470),(540,470)], RED, 9); ell((650,650,780,720), RED)
    elif art == "vase":
        poly([(390,260),(620,260),(590,760),(420,760)], fill=None if sketch else (180,210,220)); ell((385,220,625,315)); [line([(520+i*35,270),(620+i*18,160)], BLUE) for i in range(3)]
    elif art == "cap":
        line([(250,520),(420,360),(650,390),(790,520),(520,500),(250,520)]); line([(570,500),(830,560)]); line([(420,360),(450,520)], GRAY)
    elif art == "glasses":
        ell((230,390,430,590)); ell((590,390,790,590)); line([(430,490),(590,490)]); line([(230,480),(130,430)]); line([(790,480),(895,430)])
    elif art == "glove":
        line([(330,710),(310,450),(380,350),(435,490),(460,280),(520,500),(560,310),(600,520),(650,390),(650,720),(330,710)]); line([(680,520),(800,470)], RED); line([(700,580),(850,600)], RED)
    elif art == "record":
        ell((260,260,760,760)); ell((460,460,560,560)); line([(610,240),(610,550),(680,520)]); line([(670,230),(670,520)])
    elif art == "syringe":
        rect((300,430,690,540)); line([(690,485),(850,485)]); line([(245,485),(300,485)]); line([(380,430),(380,540)], (60,150,90)); line([(510,430),(510,540)], (60,150,90))
    elif art == "lamp":
        rect((250,420,760,530)); line([(270,420),(270,350),(740,350),(740,420)]); line([(350,530),(300,690)], BLUE); line([(650,530),(710,690)], BLUE); line([(420,470),(590,470)], BLUE)
    elif art == "biohazard":
        ell((420,420,600,600)); [ell((450+math.cos(a)*150-85,450+math.sin(a)*150-85,450+math.cos(a)*150+85,450+math.sin(a)*150+85)) for a in [0,2.1,4.2]]; line([(512,512),(512,780)], RED)
    elif art == "sheet":
        rect((300,180,720,820)); [line([(360,300+i*55),(660,300+i*55)], width=4) for i in range(5)]; line([(430,300),(430,540)], RED); ell((420,530,490,580), RED)
    elif art == "dog":
        poly([(220,650),(300,480),(520,420),(760,510),(820,650),(600,610),(420,680)]); ell((640,380,810,530)); ell((690,430,715,455), fill=RED); ell((750,430,775,455), fill=RED); line([(300,650),(270,800)]); line([(650,640),(720,800)])
    elif art == "warrior":
        rect((250,180,740,760)); ell((420,120,570,270)); line([(500,270),(500,620)]); line([(360,380),(640,380)]); line([(640,250),(800,720)], RED)
    elif art == "disc":
        ell((300,300,720,720), RED, width=14); ell((390,390,630,630)); rect((130,240,300,780)); line([(300,510),(720,510)], BLUE)
    elif art == "tv":
        rect((250,250,770,700)); rect((310,310,650,600)); ell((430,360,530,500)); line([(465,500),(440,580)], RED); line([(360,650),(690,650)])
    elif art == "patchbear":
        ell((310,180,710,580)); ell((240,140,390,300)); ell((630,140,780,300)); ell((430,330,590,460)); line([(510,560),(510,790)]); line([(400,650),(620,650)], RED); line([(460,690),(560,690)], RED)
    elif art == "tentacle":
        ell((380,160,640,380)); line([(510,380),(510,720)]); [line([(500,520),(300+i*80,780),(250+i*90,860)]) for i in range(4)]; line([(420,260),(600,260)], RED)
    elif art == "door":
        rect((300,150,700,850)); rect((370,230,650,830)); ell((510,430,550,470), fill=BLACK); ell((585,430,625,470), fill=BLACK); line([(650,520),(690,520)])
    elif art == "birdman":
        ell((430,130,610,300)); line([(510,300),(500,640)]); line([(390,360),(270,620)]); line([(620,360),(760,620)]); ell((260,700,420,820)); ell((560,700,720,820)); line([(470,230),(540,250),(470,270)], RED)

def make_assets():
    for id_, title, aliases, hex_color, kind, art, source, hints, data in ITEMS:
        stem = id_.lower()
        color = tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        portrait = Image.new("RGB", (W, H), (18, 20, 23))
        d = ImageDraw.Draw(portrait)
        for y in range(0, H, 64): d.line([(0, y), (W, y)], fill=(28, 31, 36), width=2)
        for x in range(0, W, 64): d.line([(x, 0), (x, H)], fill=(25, 28, 33), width=2)
        d.ellipse((90, 90, 934, 934), outline=tuple(min(255, c + 40) for c in color), width=8)
        symbol(d, art, color, sketch=False)
        portrait.save(PORTRAITS / f"{stem}.png")

        drawing = Image.new("RGB", (W, H), "white")
        symbol(ImageDraw.Draw(drawing), art, color, sketch=True)
        drawing.save(DRAWINGS / f"{stem}.png")

def regenerate_shakalized():
    for src in sorted(DRAWINGS.glob("scp-*.png")):
        base = Image.open(src).convert("RGB")
        canvas = Image.new("RGB", (W, H), "white")
        base.thumbnail((W, H), Image.Resampling.LANCZOS)
        canvas.paste(base, ((W-base.width)//2, (H-base.height)//2))
        mask = ImageOps.invert(canvas.convert("L")).point(lambda p: 255 if p > 24 else 0).filter(ImageFilter.MaxFilter(3))
        thick = Image.new("RGB", canvas.size, "white")
        thick.paste((0,0,0), mask=mask)
        canvas = Image.blend(canvas, thick, 0.28)
        for level in range(10):
            strength = (10-level)/10
            rng = random.Random(f"{src.stem}-{level}-v6")
            low = int(26 + (1-strength)*140)
            block = max(5, int(42*strength+6))
            colors = max(4, int(5+(1-strength)*24))
            quality = max(5, int(7+(1-strength)*28))
            img = canvas.resize((low, low), Image.Resampling.BOX)
            img = ImageEnhance.Contrast(img).enhance(2.1-(1-strength)*0.6)
            img = ImageEnhance.Brightness(img).enhance(0.8+(1-strength)*0.18)
            img = ImageEnhance.Color(img).enhance(0.55+(1-strength)*0.45)
            img = img.quantize(colors=colors, method=Image.Quantize.MEDIANCUT).convert("RGB")
            px = img.load()
            for y in range(0, low, block):
                for x in range(0, low, block):
                    if rng.random() < 0.26 + strength*0.38:
                        shift = rng.randint(-int(48*strength), int(48*strength))
                        for yy in range(y, min(low, y+block)):
                            for xx in range(x, min(low, x+block)):
                                r,g,b = px[xx, yy]
                                px[xx, yy] = (max(0,min(255,r+shift)), max(0,min(255,g+shift)), max(0,min(255,b+shift)))
            tmp = SHAK / f"__tmp_{src.stem}_{level}.jpg"
            img.save(tmp, quality=quality, subsampling=2, optimize=False)
            img = Image.open(tmp).convert("RGB")
            tmp.unlink(missing_ok=True)
            img = img.resize((W, H), Image.Resampling.NEAREST)
            if strength > 0.25: img = img.filter(ImageFilter.SHARPEN)
            img.save(SHAK / f"{src.stem}-{level}.png")

def update_preview():
    path = ROOT / "paint-sketches-preview.html"
    if not path.exists(): return
    text = path.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    pairs = []
    for match in re.finditer(r'id: "SCP-(\d+)"[\s\S]*?title: "([^"]+)"', script):
        pairs.append((int(match.group(1)), f"SCP-{match.group(1)}", match.group(2)))
    seen, ordered = set(), []
    for num, id_, title in sorted(pairs):
        if id_ not in seen:
            seen.add(id_)
            ordered.append((id_, title))
    arr = "      const scps = [\n" + ",\n".join(f'        ["{id_}", "{title}"]' for id_, title in ordered) + "\n      ];"
    start = text.find("      const scps = [")
    end = text.find("      ];", start)
    if start != -1 and end != -1:
        path.write_text(text[:start] + arr + text[end+8:], encoding="utf-8")

def update_credits():
    credits = CREDITS.read_text(encoding="utf-8")
    for id_, title, aliases, color, kind, art, source, hints, data in ITEMS:
        if f"<h2>{id_}</h2>" in credits:
            continue
        article = f'''
        <article>
          <h2>{id_}</h2>
          <p>
            Source: <a href="{source}" target="_blank" rel="noreferrer">{id_} on SCP Wiki</a>.
            Author: SCP Wiki contributors for the source article; SCPdle for the project portrait and Paint drawing. License: <a href="https://creativecommons.org/licenses/by-sa/3.0/" target="_blank" rel="noreferrer">CC BY-SA 3.0</a>.
          </p>
        </article>
'''
        credits = credits.replace("      </section>\n\n      <footer", article + "      </section>\n\n      <footer", 1)
    CREDITS.write_text(credits, encoding="utf-8")

if __name__ == "__main__":
    added = update_script()
    make_assets()
    regenerate_shakalized()
    update_preview()
    update_credits()
    print(f"Added {added} objects; generated assets for {len(ITEMS)} SCPs.")
