# Generated by Django 2.2.14 on 2020-07-16 04:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_candidatecv'),
    ]

    operations = [
        migrations.CreateModel(
            name='HourlyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('rate', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('currency', models.CharField(choices=[('AED', 'UAE Dirham'), ('AFN', 'Afghani'), ('ALL', 'Lek'), ('AMD', 'Armenian Dram'), ('ANG', 'Netherlands Antillean Guilder'), ('AOA', 'Kwanza'), ('ARS', 'Argentine Peso'), ('AUD', 'Australian Dollar'), ('AWG', 'Aruban Florin'), ('AZN', 'Azerbaijanian Manat'), ('BAM', 'Convertible Mark'), ('BBD', 'Barbados Dollar'), ('BDT', 'Taka'), ('BGN', 'Bulgarian Lev'), ('BHD', 'Bahraini Dinar'), ('BIF', 'Burundi Franc'), ('BMD', 'Bermudian Dollar'), ('BND', 'Brunei Dollar'), ('BOB', 'Boliviano'), ('BRL', 'Brazilian Real'), ('BSD', 'Bahamian Dollar'), ('BTN', 'Ngultrum'), ('BWP', 'Pula'), ('BYN', 'Belarusian Ruble'), ('BZD', 'Belize Dollar'), ('CAD', 'Canadian Dollar'), ('CDF', 'Congolese Franc'), ('CHF', 'Swiss Franc'), ('CLP', 'Chilean Peso'), ('CNY', 'Yuan Renminbi'), ('COP', 'Colombian Peso'), ('CRC', 'Costa Rican Colon'), ('CUC', 'Peso Convertible'), ('CUP', 'Cuban Peso'), ('CVE', 'Cabo Verde Escudo'), ('CZK', 'Czech Koruna'), ('DJF', 'Djibouti Franc'), ('DKK', 'Danish Krone'), ('DOP', 'Dominican Peso'), ('DZD', 'Algerian Dinar'), ('EGP', 'Egyptian Pound'), ('ERN', 'Nakfa'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('FJD', 'Fiji Dollar'), ('FKP', 'Falkland Islands Pound'), ('GBP', 'Pound Sterling'), ('GEL', 'Lari'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('GMD', 'Dalasi'), ('GNF', 'Guinea Franc'), ('GTQ', 'Quetzal'), ('GYD', 'Guyana Dollar'), ('HKD', 'Hong Kong Dollar'), ('HNL', 'Lempira'), ('HRK', 'Kuna'), ('HTG', 'Gourde'), ('HUF', 'Forint'), ('IDR', 'Rupiah'), ('ILS', 'New Israeli Sheqel'), ('INR', 'Indian Rupee'), ('IQD', 'Iraqi Dinar'), ('IRR', 'Iranian Rial'), ('ISK', 'Iceland Krona'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('JPY', 'Yen'), ('KES', 'Kenyan Shilling'), ('KGS', 'Som'), ('KHR', 'Riel'), ('KMF', 'Comoro Franc'), ('KPW', 'North Korean Won'), ('KRW', 'Won'), ('KWD', 'Kuwaiti Dinar'), ('KYD', 'Cayman Islands Dollar'), ('KZT', 'Tenge'), ('LAK', 'Kip'), ('LBP', 'Lebanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('LRD', 'Liberian Dollar'), ('LSL', 'Loti'), ('LYD', 'Libyan Dinar'), ('MAD', 'Moroccan Dirham'), ('MDL', 'Moldovan Leu'), ('MGA', 'Malagasy Ariary'), ('MKD', 'Denar'), ('MMK', 'Kyat'), ('MNT', 'Tugrik'), ('MOP', 'Pataca'), ('MRO', 'Ouguiya'), ('MUR', 'Mauritius Rupee'), ('MVR', 'Rufiyaa'), ('MWK', 'Malawi Kwacha'), ('MXN', 'Mexican Peso'), ('MYR', 'Malaysian Ringgit'), ('MZN', 'Mozambique Metical'), ('NAD', 'Namibia Dollar'), ('NGN', 'Naira'), ('NIO', 'Cordoba Oro'), ('NOK', 'Norwegian Krone'), ('NPR', 'Nepalese Rupee'), ('NZD', 'New Zealand Dollar'), ('OMR', 'Rial Omani'), ('PAB', 'Balboa'), ('PEN', 'Sol'), ('PGK', 'Kina'), ('PHP', 'Philippine Peso'), ('PKR', 'Pakistan Rupee'), ('PLN', 'Zloty'), ('PYG', 'Guarani'), ('QAR', 'Qatari Rial'), ('RON', 'Romanian Leu'), ('RSD', 'Serbian Dinar'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('SAR', 'Saudi Riyal'), ('SBD', 'Solomon Islands Dollar'), ('SCR', 'Seychelles Rupee'), ('SDG', 'Sudanese Pound'), ('SEK', 'Swedish Krona'), ('SGD', 'Singapore Dollar'), ('SHP', 'Saint Helena Pound'), ('SLL', 'Leone'), ('SOS', 'Somali Shilling'), ('SRD', 'Surinam Dollar'), ('SSP', 'South Sudanese Pound'), ('STD', 'Dobra'), ('SVC', 'El Salvador Colon'), ('SYP', 'Syrian Pound'), ('SZL', 'Lilangeni'), ('THB', 'Baht'), ('TJS', 'Somoni'), ('TMT', 'Turkmenistan New Manat'), ('TND', 'Tunisian Dinar'), ('TOP', 'Pa’anga'), ('TRY', 'Turkish Lira'), ('TTD', 'Trinidad and Tobago Dollar'), ('TWD', 'New Taiwan Dollar'), ('TZS', 'Tanzanian Shilling'), ('UAH', 'Hryvnia'), ('UGX', 'Uganda Shilling'), ('USD', 'US Dollar'), ('UYU', 'Peso Uruguayo'), ('UZS', 'Uzbekistan Sum'), ('VEF', 'Bolívar'), ('VND', 'Dong'), ('VUV', 'Vatu'), ('WST', 'Tala'), ('XAF', 'CFA Franc BEAC'), ('XAG', 'Silver'), ('XAU', 'Gold'), ('XBA', 'Bond Markets Unit European Composite Unit (EURCO)'), ('XBB', 'Bond Markets Unit European Monetary Unit (E.M.U.-6)'), ('XBC', 'Bond Markets Unit European Unit of Account 9 (E.U.A.-9)'), ('XBD', 'Bond Markets Unit European Unit of Account 17 (E.U.A.-17)'), ('XCD', 'East Caribbean Dollar'), ('XDR', 'SDR (Special Drawing Right)'), ('XOF', 'CFA Franc BCEAO'), ('XPD', 'Palladium'), ('XPF', 'CFP Franc'), ('XPT', 'Platinum'), ('XSU', 'Sucre'), ('XTS', 'Codes specifically reserved for testing purposes'), ('XUA', 'ADB Unit of Account'), ('XXX', 'The codes assigned for transactions where no currency is involved'), ('YER', 'Yemeni Rial'), ('ZAR', 'Rand'), ('ZMW', 'Zambian Kwacha'), ('ZWL', 'Zimbabwe Dollar')], max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='adress',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='Adress'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='city',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='City'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='country',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='nationality',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='Nationality'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='postal_code',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='Postal Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='city',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='City'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='country',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='postal_code',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='Postal Code'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'This email has been already registered in our system.'}, max_length=254, unique=True, verbose_name='Email address'),
        ),
        migrations.CreateModel(
            name='MonthlyRate',
            fields=[
                ('hourlyrate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.HourlyRate')),
            ],
            options={
                'abstract': False,
            },
            bases=('accounts.hourlyrate',),
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='hourly_rate',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hourly_rate', to='accounts.HourlyRate'),
        ),
        migrations.AddField(
            model_name='candidateprofile',
            name='monthly_rate',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monthly_rate', to='accounts.MonthlyRate'),
        ),
    ]
