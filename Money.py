# -*- coding: utf-8 -*-
from decimal import Decimal

class Currency:
	code = "XXX"
	country = ""
	countries = []
	name = ""
	numeric = "999"
	exchange_rate = Decimal("1.0")
	def __init__(self, code="", numeric="999", name="", countries=[]):
		self.code = code
		self.numeric = numeric
		self.name = name
		self.countries = countries
	def __repr__(self):
		return self.code
	def set_exchange_rate(self, rate):
		if not isinstance(rate, Decimal):
			rate = Decimal(str(rate))
		self.exchange_rate = rate

CURRENCY = {}
CURRENCY['XXX'] = Currency(code="XXX", numeric="999")
DEFAULT_CURRENCY = CURRENCY['XXX']

def set_default_currency(code="XXX"):
	global DEFAULT_CURRENCY
	DEFAULT_CURRENCY = CURRENCY[code]
	print "Default currency is now %s" % (DEFAULT_CURRENCY)

class Money:
	amount = Decimal("0.0")
	currency = DEFAULT_CURRENCY
	def __init__ (self, amount=Decimal("0.0"), currency=None):
		if not isinstance(amount, Decimal):
			amount = Decimal(str(amount))
		self.amount = amount
		if not currency:
			self.currency = DEFAULT_CURRENCY
		else:
			if not isinstance(currency, Currency):
				currency = CURRENCY[str(currency).upper()]
			self.currency = currency
	def __repr__(self):
		return '%s %5.2f' % (self.currency, self.amount)
	def __pos__(self):
		return Money(amount=self.amount, currency=self.currency)
	def __neg__(self):
		return Money(amount=-self.amount, currency=self.currency)
	def __add__(self, other):
		if isinstance(other, Money):
			if self.currency == other.currency:
				return Money(amount = self.amount + other.amount, currency = self.currency)
			else: 
				s = self.convert_to_default()
				other = other.convert_to_default()
				return Money(amount = s.amount + other.amount, currency = DEFAULT_CURRENCY)
		else:
			return Money(amount = self.amount + Decimal(str(other)), currency = self.currency)
	def __sub__(self, other):
		if isinstance(other, Money):
			if self.currency == other.currency:
				return Money(amount = self.amount - other.amount, currency = self.currency)
			else: 
				s = self.convert_to_default()
				other = other.convert_to_default()
				return Money(amount = s.amount - other.amount, currency = DEFAULT_CURRENCY)
		else:
			return Money(amount = self.amount - Decimal(str(other)), currency = self.currency)
	def __mul__(self, other):
		if isinstance(other, Money):
			raise TypeError, 'can not multiply monetary quantities'
		else:
			return Money(amount = self.amount*Decimal(str(other)), currency = self.currency)
	def __div__(self, other):
		if isinstance(other, Money):
			assert self.currency == other.currency, 'currency mismatch'
			return self.amount / other.amount
		else:
			return self.amount / Decimal(str(other))
	def __rmod__(self, other):
		"""
		Calculate percentage of an amount.  The left-hand side of the operator must be a numeric value.  E.g.:
		>>> money = Money.Money(200, "USD")
		>>> 5 % money
		USD 10.00
		"""
		if isinstance(other, Money):
			raise TypeError, 'invalid monetary operation'
		else:
			return Money(amount = Decimal(str(other)) * self.amount / 100, currency = self.currency)
	def convert_to_default(self):
		return Money(amount = self.amount * self.currency.exchange_rate, currency=DEFAULT_CURRENCY)
	def convert_to(self, currency):
		"""
		Convert from one currency to another.
		"""
		return None # TODO  (How??)
	def allocate(self, ratios):
		"""
		Allocate a sum of money to several accounts.
		"""
		total = sum(ratios)
		remainder = self.amount
		results = []
		for i in range(0, len(ratios)):
			results.append(Money(amount = self.amount * ratios[i] / total, currency = self.currency))
			remainder -= results[i].amount
		i = 0
		while i < remainder:
			results[i].amount += Decimal("0.01")
			i += 1
		return results
	def spell_out(self):
		"""
		Spell out a monetary amount.  E.g. "Two-hundred and twenty-six dollars and seventeen cents."
		"""
		pass # TODO
	
	__radd__ = __add__
	__rsub__ = __sub__
	__rmul__ = __mul__
	__rdiv__ = __div__

	#TODO: Override comparison operators


#
# Definitions of ISO 4217 Currencies
# Source: http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/currency_codes/currency_codes_list-1.htm
#

CURRENCY['BZD'] = Currency(code='BZD', numeric='084', name='Belize Dollar', countries=['BELIZE'])
CURRENCY['YER'] = Currency(code='YER', numeric='886', name='Yemeni Rial', countries=['YEMEN'])
CURRENCY['XBA'] = Currency(code='XBA', numeric='955', name='Bond Markets Units European Composite Unit (EURCO)', countries=[])
CURRENCY['SLL'] = Currency(code='SLL', numeric='694', name='Leone', countries=['SIERRA LEONE'])
CURRENCY['ERN'] = Currency(code='ERN', numeric='232', name='Nakfa', countries=['ERITREA'])
CURRENCY['NGN'] = Currency(code='NGN', numeric='566', name='Naira', countries=['NIGERIA'])
CURRENCY['CRC'] = Currency(code='CRC', numeric='188', name='Costa Rican Colon', countries=['COSTA RICA'])
CURRENCY['VEF'] = Currency(code='VEF', numeric='937', name='Bolivar Fuerte', countries=['VENEZUELA'])
CURRENCY['LAK'] = Currency(code='LAK', numeric='418', name='Kip', countries=['LAO PEOPLES DEMOCRATIC REPUBLIC'])
CURRENCY['DZD'] = Currency(code='DZD', numeric='012', name='Algerian Dinar', countries=['ALGERIA'])
CURRENCY['SZL'] = Currency(code='SZL', numeric='748', name='Lilangeni', countries=['SWAZILAND'])
CURRENCY['MOP'] = Currency(code='MOP', numeric='446', name='Pataca', countries=['MACAO'])
CURRENCY['BYR'] = Currency(code='BYR', numeric='974', name='Belarussian Ruble', countries=['BELARUS'])
CURRENCY['MUR'] = Currency(code='MUR', numeric='480', name='Mauritius Rupee', countries=['MAURITIUS'])
CURRENCY['WST'] = Currency(code='WST', numeric='882', name='Tala', countries=['SAMOA'])
CURRENCY['LRD'] = Currency(code='LRD', numeric='430', name='Liberian Dollar', countries=['LIBERIA'])
CURRENCY['MMK'] = Currency(code='MMK', numeric='104', name='Kyat', countries=['MYANMAR'])
CURRENCY['KGS'] = Currency(code='KGS', numeric='417', name='Som', countries=['KYRGYZSTAN'])
CURRENCY['PYG'] = Currency(code='PYG', numeric='600', name='Guarani', countries=['PARAGUAY'])
CURRENCY['IDR'] = Currency(code='IDR', numeric='360', name='Rupiah', countries=['INDONESIA'])
CURRENCY['XBD'] = Currency(code='XBD', numeric='958', name='European Unit of Account 17(E.U.A.-17)', countries=[])
CURRENCY['GTQ'] = Currency(code='GTQ', numeric='320', name='Quetzal', countries=['GUATEMALA'])
CURRENCY['CAD'] = Currency(code='CAD', numeric='124', name='Canadian Dollar', countries=['CANADA'])
CURRENCY['AWG'] = Currency(code='AWG', numeric='533', name='Aruban Guilder', countries=['ARUBA'])
CURRENCY['TTD'] = Currency(code='TTD', numeric='780', name='Trinidad and Tobago Dollar', countries=['TRINIDAD AND TOBAGO'])
CURRENCY['PKR'] = Currency(code='PKR', numeric='586', name='Pakistan Rupee', countries=['PAKISTAN'])
CURRENCY['XBC'] = Currency(code='XBC', numeric='957', name='European Unit of Account 9(E.U.A.-9)', countries=[])
CURRENCY['UZS'] = Currency(code='UZS', numeric='860', name='Uzbekistan Sum', countries=['UZBEKISTAN'])
CURRENCY['XCD'] = Currency(code='XCD', numeric='951', name='East Caribbean Dollar', countries=['ANGUILLA', 'ANTIGUA AND BARBUDA', 'DOMINICA', 'GRENADA', 'MONTSERRAT', 'SAINT KITTS AND NEVIS', 'SAINT LUCIA', 'SAINT VINCENT AND THE GRENADINES'])
CURRENCY['VUV'] = Currency(code='VUV', numeric='548', name='Vatu', countries=['VANUATU'])
CURRENCY['KMF'] = Currency(code='KMF', numeric='174', name='Comoro Franc', countries=['COMOROS'])
CURRENCY['AZN'] = Currency(code='AZN', numeric='944', name='Azerbaijanian Manat', countries=['AZERBAIJAN'])
CURRENCY['XPD'] = Currency(code='XPD', numeric='964', name='Palladium', countries=[])
CURRENCY['MNT'] = Currency(code='MNT', numeric='496', name='Tugrik', countries=['MONGOLIA'])
CURRENCY['ANG'] = Currency(code='ANG', numeric='532', name='Netherlands Antillian Guilder', countries=['NETHERLANDS ANTILLES'])
CURRENCY['LBP'] = Currency(code='LBP', numeric='422', name='Lebanese Pound', countries=['LEBANON'])
CURRENCY['KES'] = Currency(code='KES', numeric='404', name='Kenyan Shilling', countries=['KENYA'])
CURRENCY['GBP'] = Currency(code='GBP', numeric='826', name='Pound Sterling', countries=['UNITED KINGDOM'])
CURRENCY['SEK'] = Currency(code='SEK', numeric='752', name='Swedish Krona', countries=['SWEDEN'])
CURRENCY['AFN'] = Currency(code='AFN', numeric='971', name='Afghani', countries=['AFGHANISTAN'])
CURRENCY['KZT'] = Currency(code='KZT', numeric='398', name='Tenge', countries=['KAZAKHSTAN'])
CURRENCY['ZMK'] = Currency(code='ZMK', numeric='894', name='Kwacha', countries=['ZAMBIA'])
CURRENCY['SKK'] = Currency(code='SKK', numeric='703', name='Slovak Koruna', countries=['SLOVAKIA'])
CURRENCY['DKK'] = Currency(code='DKK', numeric='208', name='Danish Krone', countries=['DENMARK', 'FAROE ISLANDS', 'GREENLAND'])
CURRENCY['TMM'] = Currency(code='TMM', numeric='795', name='Manat', countries=['TURKMENISTAN'])
CURRENCY['AMD'] = Currency(code='AMD', numeric='051', name='Armenian Dram', countries=['ARMENIA'])
CURRENCY['SCR'] = Currency(code='SCR', numeric='690', name='Seychelles Rupee', countries=['SEYCHELLES'])
CURRENCY['FJD'] = Currency(code='FJD', numeric='242', name='Fiji Dollar', countries=['FIJI'])
CURRENCY['SHP'] = Currency(code='SHP', numeric='654', name='Saint Helena Pound', countries=['SAINT HELENA'])
CURRENCY['ALL'] = Currency(code='ALL', numeric='008', name='Lek', countries=['ALBANIA'])
CURRENCY['TOP'] = Currency(code='TOP', numeric='776', name='Paanga', countries=['TONGA'])
CURRENCY['UGX'] = Currency(code='UGX', numeric='800', name='Uganda Shilling', countries=['UGANDA'])
CURRENCY['OMR'] = Currency(code='OMR', numeric='512', name='Rial Omani', countries=['OMAN'])
CURRENCY['DJF'] = Currency(code='DJF', numeric='262', name='Djibouti Franc', countries=['DJIBOUTI'])
CURRENCY['BND'] = Currency(code='BND', numeric='096', name='Brunei Dollar', countries=['BRUNEI DARUSSALAM'])
CURRENCY['TND'] = Currency(code='TND', numeric='788', name='Tunisian Dinar', countries=['TUNISIA'])
CURRENCY['SBD'] = Currency(code='SBD', numeric='090', name='Solomon Islands Dollar', countries=['SOLOMON ISLANDS'])
CURRENCY['GHS'] = Currency(code='GHS', numeric='936', name='Ghana Cedi', countries=['GHANA'])
CURRENCY['GNF'] = Currency(code='GNF', numeric='324', name='Guinea Franc', countries=['GUINEA'])
CURRENCY['CVE'] = Currency(code='CVE', numeric='132', name='Cape Verde Escudo', countries=['CAPE VERDE'])
CURRENCY['ARS'] = Currency(code='ARS', numeric='032', name='Argentine Peso', countries=['ARGENTINA'])
CURRENCY['GMD'] = Currency(code='GMD', numeric='270', name='Dalasi', countries=['GAMBIA'])
CURRENCY['ZWD'] = Currency(code='ZWD', numeric='716', name='Zimbabwe Dollar', countries=['ZIMBABWE'])
CURRENCY['MWK'] = Currency(code='MWK', numeric='454', name='Kwacha', countries=['MALAWI'])
CURRENCY['BDT'] = Currency(code='BDT', numeric='050', name='Taka', countries=['BANGLADESH'])
CURRENCY['KWD'] = Currency(code='KWD', numeric='414', name='Kuwaiti Dinar', countries=['KUWAIT'])
CURRENCY['EUR'] = Currency(code='EUR', numeric='978', name='Euro', countries=['ANDORRA', 'AUSTRIA', 'BELGIUM', 'FINLAND', 'FRANCE', 'FRENCH GUIANA', 'FRENCH SOUTHERN TERRITORIES', 'GERMANY', 'GREECE', 'GUADELOUPE', 'IRELAND', 'ITALY', 'LUXEMBOURG', 'MARTINIQUE', 'MAYOTTE', 'MONACO', 'MONTENEGRO', 'NETHERLANDS', 'PORTUGAL', 'R.UNION', 'SAINT PIERRE AND MIQUELON', 'SAN MARINO', 'SLOVENIA', 'SPAIN'])
CURRENCY['CHF'] = Currency(code='CHF', numeric='756', name='Swiss Franc', countries=['LIECHTENSTEIN'])
CURRENCY['XAG'] = Currency(code='XAG', numeric='961', name='Silver', countries=[])
CURRENCY['SRD'] = Currency(code='SRD', numeric='968', name='Surinam Dollar', countries=['SURINAME'])
CURRENCY['DOP'] = Currency(code='DOP', numeric='214', name='Dominican Peso', countries=['DOMINICAN REPUBLIC'])
CURRENCY['PEN'] = Currency(code='PEN', numeric='604', name='Nuevo Sol', countries=['PERU'])
CURRENCY['KPW'] = Currency(code='KPW', numeric='408', name='North Korean Won', countries=['KOREA'])
CURRENCY['SGD'] = Currency(code='SGD', numeric='702', name='Singapore Dollar', countries=['SINGAPORE'])
CURRENCY['TWD'] = Currency(code='TWD', numeric='901', name='New Taiwan Dollar', countries=['TAIWAN'])
CURRENCY['USD'] = Currency(code='USD', numeric='840', name='US Dollar', countries=['AMERICAN SAMOA', 'BRITISH INDIAN OCEAN TERRITORY', 'ECUADOR', 'GUAM', 'MARSHALL ISLANDS', 'MICRONESIA', 'NORTHERN MARIANA ISLANDS', 'PALAU', 'PUERTO RICO', 'TIMOR-LESTE', 'TURKS AND CAICOS ISLANDS', 'UNITED STATES MINOR OUTLYING ISLANDS', 'VIRGIN ISLANDS (BRITISH)', 'VIRGIN ISLANDS (U.S.)'])
CURRENCY['BGN'] = Currency(code='BGN', numeric='975', name='Bulgarian Lev', countries=['BULGARIA'])
CURRENCY['MAD'] = Currency(code='MAD', numeric='504', name='Moroccan Dirham', countries=['MOROCCO', 'WESTERN SAHARA'])
CURRENCY['XXX'] = Currency(code='XXX', numeric='999', name='The codes assigned for transactions where no currency is involved are:', countries=[])
CURRENCY['SAR'] = Currency(code='SAR', numeric='682', name='Saudi Riyal', countries=['SAUDI ARABIA'])
CURRENCY['AUD'] = Currency(code='AUD', numeric='036', name='Australian Dollar', countries=['AUSTRALIA', 'CHRISTMAS ISLAND', 'COCOS (KEELING) ISLANDS', 'HEARD ISLAND AND MCDONALD ISLANDS', 'KIRIBATI', 'NAURU', 'NORFOLK ISLAND', 'TUVALU'])
CURRENCY['KYD'] = Currency(code='KYD', numeric='136', name='Cayman Islands Dollar', countries=['CAYMAN ISLANDS'])
CURRENCY['KRW'] = Currency(code='KRW', numeric='410', name='Won', countries=['KOREA'])
CURRENCY['GIP'] = Currency(code='GIP', numeric='292', name='Gibraltar Pound', countries=['GIBRALTAR'])
CURRENCY['TRY'] = Currency(code='TRY', numeric='949', name='New Turkish Lira', countries=['TURKEY'])
CURRENCY['XAU'] = Currency(code='XAU', numeric='959', name='Gold', countries=[])
CURRENCY['CZK'] = Currency(code='CZK', numeric='203', name='Czech Koruna', countries=['CZECH REPUBLIC'])
CURRENCY['JMD'] = Currency(code='JMD', numeric='388', name='Jamaican Dollar', countries=['JAMAICA'])
CURRENCY['BSD'] = Currency(code='BSD', numeric='044', name='Bahamian Dollar', countries=['BAHAMAS'])
CURRENCY['BWP'] = Currency(code='BWP', numeric='072', name='Pula', countries=['BOTSWANA'])
CURRENCY['GYD'] = Currency(code='GYD', numeric='328', name='Guyana Dollar', countries=['GUYANA'])
CURRENCY['XTS'] = Currency(code='XTS', numeric='963', name='Codes specifically reserved for testing purposes', countries=[])
CURRENCY['LYD'] = Currency(code='LYD', numeric='434', name='Libyan Dinar', countries=['LIBYAN ARAB JAMAHIRIYA'])
CURRENCY['EGP'] = Currency(code='EGP', numeric='818', name='Egyptian Pound', countries=['EGYPT'])
CURRENCY['THB'] = Currency(code='THB', numeric='764', name='Baht', countries=['THAILAND'])
CURRENCY['MKD'] = Currency(code='MKD', numeric='807', name='Denar', countries=['MACEDONIA'])
CURRENCY['SDG'] = Currency(code='SDG', numeric='938', name='Sudanese Pound', countries=['SUDAN'])
CURRENCY['AED'] = Currency(code='AED', numeric='784', name='UAE Dirham', countries=['UNITED ARAB EMIRATES'])
CURRENCY['JOD'] = Currency(code='JOD', numeric='400', name='Jordanian Dinar', countries=['JORDAN'])
CURRENCY['JPY'] = Currency(code='JPY', numeric='392', name='Yen', countries=['JAPAN'])
CURRENCY['ZAR'] = Currency(code='ZAR', numeric='710', name='Rand', countries=['SOUTH AFRICA'])
CURRENCY['HRK'] = Currency(code='HRK', numeric='191', name='Croatian Kuna', countries=['CROATIA'])
CURRENCY['AOA'] = Currency(code='AOA', numeric='973', name='Kwanza', countries=['ANGOLA'])
CURRENCY['RWF'] = Currency(code='RWF', numeric='646', name='Rwanda Franc', countries=['RWANDA'])
CURRENCY['CUP'] = Currency(code='CUP', numeric='192', name='Cuban Peso', countries=['CUBA'])
CURRENCY['XFO'] = Currency(code='XFO', numeric='Nil', name='Gold-Franc', countries=[])
CURRENCY['BBD'] = Currency(code='BBD', numeric='052', name='Barbados Dollar', countries=['BARBADOS'])
CURRENCY['PGK'] = Currency(code='PGK', numeric='598', name='Kina', countries=['PAPUA NEW GUINEA'])
CURRENCY['LKR'] = Currency(code='LKR', numeric='144', name='Sri Lanka Rupee', countries=['SRI LANKA'])
CURRENCY['RON'] = Currency(code='RON', numeric='946', name='New Leu', countries=['ROMANIA'])
CURRENCY['PLN'] = Currency(code='PLN', numeric='985', name='Zloty', countries=['POLAND'])
CURRENCY['IQD'] = Currency(code='IQD', numeric='368', name='Iraqi Dinar', countries=['IRAQ'])
CURRENCY['TJS'] = Currency(code='TJS', numeric='972', name='Somoni', countries=['TAJIKISTAN'])
CURRENCY['MDL'] = Currency(code='MDL', numeric='498', name='Moldovan Leu', countries=['MOLDOVA'])
CURRENCY['MYR'] = Currency(code='MYR', numeric='458', name='Malaysian Ringgit', countries=['MALAYSIA'])
CURRENCY['CNY'] = Currency(code='CNY', numeric='156', name='Yuan Renminbi', countries=['CHINA'])
CURRENCY['LVL'] = Currency(code='LVL', numeric='428', name='Latvian Lats', countries=['LATVIA'])
CURRENCY['INR'] = Currency(code='INR', numeric='356', name='Indian Rupee', countries=['INDIA'])
CURRENCY['FKP'] = Currency(code='FKP', numeric='238', name='Falkland Islands Pound', countries=['FALKLAND ISLANDS (MALVINAS)'])
CURRENCY['NIO'] = Currency(code='NIO', numeric='558', name='Cordoba Oro', countries=['NICARAGUA'])
CURRENCY['PHP'] = Currency(code='PHP', numeric='608', name='Philippine Peso', countries=['PHILIPPINES'])
CURRENCY['HNL'] = Currency(code='HNL', numeric='340', name='Lempira', countries=['HONDURAS'])
CURRENCY['HKD'] = Currency(code='HKD', numeric='344', name='Hong Kong Dollar', countries=['HONG KONG'])
CURRENCY['NZD'] = Currency(code='NZD', numeric='554', name='New Zealand Dollar', countries=['COOK ISLANDS', 'NEW ZEALAND', 'NIUE', 'PITCAIRN', 'TOKELAU'])
CURRENCY['BRL'] = Currency(code='BRL', numeric='986', name='Brazilian Real', countries=['BRAZIL'])
CURRENCY['RSD'] = Currency(code='RSD', numeric='941', name='Serbian Dinar', countries=['SERBIA'])
CURRENCY['XBB'] = Currency(code='XBB', numeric='956', name='European Monetary Unit (E.M.U.-6)', countries=[])
CURRENCY['EEK'] = Currency(code='EEK', numeric='233', name='Kroon', countries=['ESTONIA'])
CURRENCY['SOS'] = Currency(code='SOS', numeric='706', name='Somali Shilling', countries=['SOMALIA'])
CURRENCY['MZN'] = Currency(code='MZN', numeric='943', name='Metical', countries=['MOZAMBIQUE'])
CURRENCY['XFU'] = Currency(code='XFU', numeric='Nil', name='UIC-Franc', countries=[])
CURRENCY['NOK'] = Currency(code='NOK', numeric='578', name='Norwegian Krone', countries=['BOUVET ISLAND', 'NORWAY', 'SVALBARD AND JAN MAYEN'])
CURRENCY['ISK'] = Currency(code='ISK', numeric='352', name='Iceland Krona', countries=['ICELAND'])
CURRENCY['GEL'] = Currency(code='GEL', numeric='981', name='Lari', countries=['GEORGIA'])
CURRENCY['ILS'] = Currency(code='ILS', numeric='376', name='New Israeli Sheqel', countries=['ISRAEL'])
CURRENCY['HUF'] = Currency(code='HUF', numeric='348', name='Forint', countries=['HUNGARY'])
CURRENCY['UAH'] = Currency(code='UAH', numeric='980', name='Hryvnia', countries=['UKRAINE'])
CURRENCY['RUB'] = Currency(code='RUB', numeric='643', name='Russian Ruble', countries=['RUSSIAN FEDERATION'])
CURRENCY['IRR'] = Currency(code='IRR', numeric='364', name='Iranian Rial', countries=['IRAN'])
CURRENCY['BMD'] = Currency(code='BMD', numeric='060', name='Bermudian Dollar (customarily known as Bermuda Dollar)', countries=['BERMUDA'])
CURRENCY['MGA'] = Currency(code='MGA', numeric='969', name='Malagasy Ariary', countries=['MADAGASCAR'])
CURRENCY['MVR'] = Currency(code='MVR', numeric='462', name='Rufiyaa', countries=['MALDIVES'])
CURRENCY['QAR'] = Currency(code='QAR', numeric='634', name='Qatari Rial', countries=['QATAR'])
CURRENCY['VND'] = Currency(code='VND', numeric='704', name='Dong', countries=['VIET NAM'])
CURRENCY['MRO'] = Currency(code='MRO', numeric='478', name='Ouguiya', countries=['MAURITANIA'])
CURRENCY['NPR'] = Currency(code='NPR', numeric='524', name='Nepalese Rupee', countries=['NEPAL'])
CURRENCY['TZS'] = Currency(code='TZS', numeric='834', name='Tanzanian Shilling', countries=['TANZANIA'])
CURRENCY['BIF'] = Currency(code='BIF', numeric='108', name='Burundi Franc', countries=['BURUNDI'])
CURRENCY['XPT'] = Currency(code='XPT', numeric='962', name='Platinum', countries=[])
CURRENCY['KHR'] = Currency(code='KHR', numeric='116', name='Riel', countries=['CAMBODIA'])
CURRENCY['SYP'] = Currency(code='SYP', numeric='760', name='Syrian Pound', countries=['SYRIAN ARAB REPUBLIC'])
CURRENCY['BHD'] = Currency(code='BHD', numeric='048', name='Bahraini Dinar', countries=['BAHRAIN'])
CURRENCY['XDR'] = Currency(code='XDR', numeric='960', name='SDR', countries=['INTERNATIONAL MONETARY FUND (I.M.F)'])
CURRENCY['STD'] = Currency(code='STD', numeric='678', name='Dobra', countries=['SAO TOME AND PRINCIPE'])
CURRENCY['BAM'] = Currency(code='BAM', numeric='977', name='Convertible Marks', countries=['BOSNIA AND HERZEGOVINA'])
CURRENCY['LTL'] = Currency(code='LTL', numeric='440', name='Lithuanian Litas', countries=['LITHUANIA'])
CURRENCY['ETB'] = Currency(code='ETB', numeric='230', name='Ethiopian Birr', countries=['ETHIOPIA'])
CURRENCY['XPF'] = Currency(code='XPF', numeric='953', name='CFP Franc', countries=['FRENCH POLYNESIA', 'NEW CALEDONIA', 'WALLIS AND FUTUNA'])
