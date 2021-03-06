# Generated by Django 2.2.12 on 2020-05-20 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200519_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_logo', models.ImageField(blank=True, upload_to='company_logo', verbose_name='Logo')),
                ('company_name', models.CharField(max_length=255, verbose_name='Name')),
                ('company_adress', models.CharField(max_length=255, verbose_name='Adress')),
                ('company_description', models.TextField(blank=True, verbose_name='Description')),
                ('company_size', models.IntegerField(choices=[(1, '<50'), (2, '50-200'), (3, '200-500'), (4, '500+')], verbose_name='Company Size')),
                ('company_website', models.URLField(max_length=255, verbose_name='Website')),
                ('language', models.CharField(choices=[('aa', 'Afar'), ('ab', 'Abkhazian'), ('af', 'Afrikaans'), ('ak', 'Akan'), ('am', 'Amharic'), ('ar', 'Arabic'), ('an', 'Aragonese'), ('as', 'Assamese'), ('av', 'Avaric'), ('ae', 'Avestan'), ('ay', 'Aymara'), ('az', 'Azerbaijani'), ('ba', 'Bashkir'), ('bm', 'Bambara'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('bi', 'Bislama'), ('bo', 'Tibetan'), ('bs', 'Bosnian'), ('br', 'Breton'), ('bg', 'Bulgarian'), ('ca', 'Catalan'), ('cs', 'Czech'), ('ch', 'Chamorro'), ('ce', 'Chechen'), ('cu', 'Church Slavic'), ('cv', 'Chuvash'), ('kw', 'Cornish'), ('co', 'Corsican'), ('cr', 'Cree'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dv', 'Dhivehi'), ('dz', 'Dzongkha'), ('el', 'Modern Greek (1453-)'), ('en', 'English'), ('eo', 'Esperanto'), ('et', 'Estonian'), ('eu', 'Basque'), ('ee', 'Ewe'), ('fo', 'Faroese'), ('fa', 'Persian'), ('fj', 'Fijian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Western Frisian'), ('ff', 'Fulah'), ('gd', 'Scottish Gaelic'), ('ga', 'Irish'), ('gl', 'Galician'), ('gv', 'Manx'), ('gn', 'Guarani'), ('gu', 'Gujarati'), ('ht', 'Haitian'), ('ha', 'Hausa'), ('sh', 'Serbo-Croatian'), ('he', 'Hebrew'), ('hz', 'Herero'), ('hi', 'Hindi'), ('ho', 'Hiri Motu'), ('hr', 'Croatian'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('ig', 'Igbo'), ('io', 'Ido'), ('ii', 'Sichuan Yi'), ('iu', 'Inuktitut'), ('ie', 'Interlingue'), ('ia', 'Interlingua (International Auxiliary Language Association)'), ('id', 'Indonesian'), ('ik', 'Inupiaq'), ('is', 'Icelandic'), ('it', 'Italian'), ('jv', 'Javanese'), ('ja', 'Japanese'), ('kl', 'Kalaallisut'), ('kn', 'Kannada'), ('ks', 'Kashmiri'), ('ka', 'Georgian'), ('kr', 'Kanuri'), ('kk', 'Kazakh'), ('km', 'Central Khmer'), ('ki', 'Kikuyu'), ('rw', 'Kinyarwanda'), ('ky', 'Kirghiz'), ('kv', 'Komi'), ('kg', 'Kongo'), ('ko', 'Korean'), ('kj', 'Kuanyama'), ('ku', 'Kurdish'), ('lo', 'Lao'), ('la', 'Latin'), ('lv', 'Latvian'), ('li', 'Limburgan'), ('ln', 'Lingala'), ('lt', 'Lithuanian'), ('lb', 'Luxembourgish'), ('lu', 'Luba-Katanga'), ('lg', 'Ganda'), ('mh', 'Marshallese'), ('ml', 'Malayalam'), ('mr', 'Marathi'), ('mk', 'Macedonian'), ('mg', 'Malagasy'), ('mt', 'Maltese'), ('mn', 'Mongolian'), ('mi', 'Maori'), ('ms', 'Malay (macrolanguage)'), ('my', 'Burmese'), ('na', 'Nauru'), ('nv', 'Navajo'), ('nr', 'South Ndebele'), ('nd', 'North Ndebele'), ('ng', 'Ndonga'), ('ne', 'Nepali (macrolanguage)'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('nb', 'Norwegian Bokmål'), ('no', 'Norwegian'), ('ny', 'Nyanja'), ('oc', 'Occitan (post 1500)'), ('oj', 'Ojibwa'), ('or', 'Oriya (macrolanguage)'), ('om', 'Oromo'), ('os', 'Ossetian'), ('pa', 'Panjabi'), ('pi', 'Pali'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('ps', 'Pushto'), ('qu', 'Quechua'), ('rm', 'Romansh'), ('ro', 'Romanian'), ('rn', 'Rundi'), ('ru', 'Russian'), ('sg', 'Sango'), ('sa', 'Sanskrit'), ('si', 'Sinhala'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('se', 'Northern Sami'), ('sm', 'Samoan'), ('sn', 'Shona'), ('sd', 'Sindhi'), ('so', 'Somali'), ('st', 'Southern Sotho'), ('es', 'Spanish'), ('sq', 'Albanian'), ('sc', 'Sardinian'), ('sr', 'Serbian'), ('ss', 'Swati'), ('su', 'Sundanese'), ('sw', 'Swahili (macrolanguage)'), ('sv', 'Swedish'), ('ty', 'Tahitian'), ('ta', 'Tamil'), ('tt', 'Tatar'), ('te', 'Telugu'), ('tg', 'Tajik'), ('tl', 'Tagalog'), ('th', 'Thai'), ('ti', 'Tigrinya'), ('to', 'Tonga (Tonga Islands)'), ('tn', 'Tswana'), ('ts', 'Tsonga'), ('tk', 'Turkmen'), ('tr', 'Turkish'), ('tw', 'Twi'), ('ug', 'Uighur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('ve', 'Venda'), ('vi', 'Vietnamese'), ('vo', 'Volapük'), ('wa', 'Walloon'), ('wo', 'Wolof'), ('xh', 'Xhosa'), ('yi', 'Yiddish'), ('yo', 'Yoruba'), ('za', 'Zhuang'), ('zh', 'Chinese'), ('zu', 'Zulu')], max_length=2, verbose_name='Communication Language')),
            ],
            options={
                'verbose_name': 'comany profile',
                'verbose_name_plural': 'company profiles',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date joined'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'Company'), (2, 'Candidate')], null=True, verbose_name='User type'),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, max_length=255, verbose_name='Link url')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='additional_links', to='accounts.CompanyProfile', verbose_name='Company')),
            ],
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, verbose_name='Phone number')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email address')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_persons', to='accounts.CompanyProfile', verbose_name='Company')),
            ],
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
