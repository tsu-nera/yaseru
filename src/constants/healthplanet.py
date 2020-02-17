##################
# Health Planet
##################

# API仕様 ver1.0
# https://www.healthplanet.jp/apis/api.html

HP_HOST = 'www.healthplanet.jp'
HP_REDIRECT_URI = 'https://www.healthplanet.jp/success.html'
HP_DEFAULT_SCOPE = 'innerscan'
HP_DEFAULT_RESPONSE_TYPE = 'code'
HP_DEFAULT_GRANT_TYPE = 'authorization_code'


HP_DATE_TYPE_REGISTER = 0  # 登録日付
HP_DATE_TYPE_RECORD = 1  # 計測日付

HP_TAG_WEIGHT = 6021  # 体重 (kg)
HP_TAG_BODY_FAT_PARCENTAGE = 6022  # 体脂肪率 (%)
HP_TAG_MUSCLE_MASS = 6023  # 筋肉量 (kg)
HP_TAG_MUSCLE_SCORE = 6024  # 筋肉スコア
HP_TAG_VISCERAL_FAT_LEVEL = 6025  # 内臓脂肪レベル2(小数点有り、手入力含まず)
HP_TAG_VISCERAL_FAT_LEVEL2 = 6026  # 内臓脂肪レベル(小数点無し、手入力含む)
HP_TAG_BASAL_METABOLIC_RATE = 6027  # 基礎代謝量(kcal)
HP_TAG_BODY_AGE = 6028  # 体内年齢(才)
HP_TAG_ESTIMATED_BONE_MASS = 6029  # 推定骨量(kg)
