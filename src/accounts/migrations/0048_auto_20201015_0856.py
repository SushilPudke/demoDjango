# Generated by Django 2.2.16 on 2020-10-15 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0047_merge_20201012_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencyprofile',
            name='country',
            field=models.CharField(choices=[('af', 'Afghanistan'), ('al', 'Albania'), ('dz', 'Algeria'), ('ad', 'Andorra'), ('ao', 'Angola'), ('ag', 'Antigua and Barbuda'), ('ar', 'Argentina'), ('am', 'Armenia'), ('aw', 'Aruba'), ('au', 'Australia'), ('at', 'Austria'), ('az', 'Azerbaijan'), ('bs', 'Bahamas'), ('bh', 'Bahrain'), ('bd', 'Bangladesh'), ('bb', 'Barbados'), ('by', 'Belarus'), ('be', 'Belgium'), ('bz', 'Belize'), ('bj', 'Benin'), ('bt', 'Bhutan'), ('bo', 'Bolivia'), ('ba', 'Bosnia and Herzegovina'), ('bw', 'Botswana'), ('br', 'Brazil'), ('io', 'British Indian Ocean Territory'), ('bn', 'Brunei'), ('bg', 'Bulgaria'), ('bf', 'Burkina Faso'), ('bi', 'Burundi'), ('kh', 'Cambodia'), ('cm', 'Cameroon'), ('ca', 'Canada'), ('cv', 'Cape Verde'), ('bq', 'Caribbean Netherlands'), ('cf', 'Central African Republic'), ('td', 'Chad'), ('cl', 'Chile'), ('cn', 'China'), ('co', 'Colombia'), ('km', 'Comoros'), ('cd', 'Congo-Kinshasa'), ('cg', 'Congo-Brazzaville'), ('cr', 'Costa Rica'), ('ci', 'Côte d’Ivoire'), ('hr', 'Croatia'), ('cu', 'Cuba'), ('cw', 'Curaçao'), ('cy', 'Cyprus'), ('cz', 'Czech Republic'), ('dk', 'Denmark'), ('dj', 'Djibouti'), ('dm', 'Dominica'), ('do', 'Dominican Republic'), ('ec', 'Ecuador'), ('eg', 'Egypt'), ('sv', 'El Salvador'), ('gq', 'Equatorial Guinea'), ('er', 'Eritrea'), ('ee', 'Estonia'), ('et', 'Ethiopia'), ('fj', 'Fiji'), ('fi', 'Finland'), ('fr', 'France'), ('gf', 'French Guiana'), ('pf', 'French Polynesia'), ('ga', 'Gabon'), ('gm', 'Gambia'), ('ge', 'Georgia'), ('de', 'Germany'), ('gh', 'Ghana'), ('gr', 'Greece'), ('gd', 'Grenada'), ('gp', 'Guadeloupe'), ('gu', 'Guam'), ('gt', 'Guatemala'), ('gn', 'Guinea'), ('gw', 'Guinea-Bissau'), ('gy', 'Guyana'), ('ht', 'Haiti'), ('hn', 'Honduras'), ('hk', 'Hong Kong'), ('hu', 'Hungary'), ('is', 'Iceland'), ('in', 'India'), ('id', 'Indonesia'), ('ir', 'Iran'), ('iq', 'Iraq'), ('ie', 'Ireland'), ('il', 'Israel'), ('it', 'Italy'), ('jm', 'Jamaica'), ('jp', 'Japan'), ('jo', 'Jordan'), ('kz', 'Kazakhstan'), ('ke', 'Kenya'), ('ki', 'Kiribati'), ('xk', 'Kosovo'), ('kw', 'Kuwait'), ('kg', 'Kyrgyzstan'), ('la', 'Laos'), ('lv', 'Latvia'), ('lb', 'Lebanon'), ('ls', 'Lesotho'), ('lr', 'Liberia'), ('ly', 'Libya'), ('li', 'Liechtenstein'), ('lt', 'Lithuania'), ('lu', 'Luxembourg'), ('mo', 'Macau'), ('mk', 'Macedonia'), ('mg', 'Madagascar'), ('mw', 'Malawi'), ('my', 'Malaysia'), ('mv', 'Maldives'), ('ml', 'Mali'), ('mt', 'Malta'), ('mh', 'Marshall Islands'), ('mq', 'Martinique'), ('mr', 'Mauritania'), ('mu', 'Mauritius'), ('mx', 'Mexico'), ('fm', 'Micronesia'), ('md', 'Moldova'), ('mc', 'Monaco'), ('mn', 'Mongolia'), ('me', 'Montenegro'), ('ma', 'Morocco'), ('mz', 'Mozambique'), ('mm', 'Myanmar'), ('na', 'Namibia'), ('nr', 'Nauru'), ('np', 'Nepal'), ('nl', 'Netherlands'), ('nc', 'New Caledonia'), ('nz', 'New Zealand'), ('ni', 'Nicaragua'), ('ne', 'Niger'), ('ng', 'Nigeria'), ('kp', 'North Korea'), ('no', 'Norway'), ('om', 'Oman'), ('pk', 'Pakistan'), ('pw', 'Palau'), ('ps', 'Palestine'), ('pa', 'Panama'), ('pg', 'Papua New Guinea'), ('py', 'Paraguay'), ('pe', 'Peru'), ('ph', 'Philippines'), ('pl', 'Poland'), ('pt', 'Portugal'), ('pr', 'Puerto Rico'), ('qa', 'Qatar'), ('re', 'Réunion'), ('ro', 'Romania'), ('ru', 'Russia'), ('rw', 'Rwanda'), ('kn', 'Saint Kitts and Nevis'), ('lc', 'Saint Lucia'), ('vc', 'Saint Vincent and the Grenadines'), ('ws', 'Samoa'), ('sm', 'San Marino'), ('st', 'São Tomé and Príncipe'), ('sa', 'Saudi Arabia'), ('sn', 'Senegal'), ('rs', 'Serbia'), ('sc', 'Seychelles'), ('sl', 'Sierra Leone'), ('sg', 'Singapore'), ('sk', 'Slovakia'), ('si', 'Slovenia'), ('sb', 'Solomon Islands'), ('so', 'Somalia'), ('za', 'South Africa'), ('kr', 'South Korea'), ('ss', 'South Sudan'), ('es', 'Spain'), ('lk', 'Sri Lanka'), ('sd', 'Sudan'), ('sr', 'Suriname'), ('sz', 'Swaziland'), ('se', 'Sweden'), ('ch', 'Switzerland'), ('sy', 'Syria'), ('tw', 'Taiwan'), ('tj', 'Tajikistan'), ('tz', 'Tanzania'), ('th', 'Thailand'), ('tl', 'Timor-Leste'), ('tg', 'Togo'), ('to', 'Tonga'), ('tt', 'Trinidad and Tobago'), ('tn', 'Tunisia'), ('tr', 'Turkey'), ('tm', 'Turkmenistan'), ('tv', 'Tuvalu'), ('ug', 'Uganda'), ('ua', 'Ukraine'), ('ae', 'United Arab Emirates'), ('gb', 'United Kingdom'), ('us', 'United States'), ('uy', 'Uruguay'), ('uz', 'Uzbekistan'), ('vu', 'Vanuatu'), ('va', 'Vatican City'), ('ve', 'Venezuela'), ('vn', 'Vietnam'), ('ye', 'Yemen'), ('zm', 'Zambia'), ('zw', 'Zimbabwe')], db_index=True, max_length=255, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='agencyprofile',
            name='country_de',
            field=models.CharField(choices=[('af', 'Afghanistan'), ('al', 'Albania'), ('dz', 'Algeria'), ('ad', 'Andorra'), ('ao', 'Angola'), ('ag', 'Antigua and Barbuda'), ('ar', 'Argentina'), ('am', 'Armenia'), ('aw', 'Aruba'), ('au', 'Australia'), ('at', 'Austria'), ('az', 'Azerbaijan'), ('bs', 'Bahamas'), ('bh', 'Bahrain'), ('bd', 'Bangladesh'), ('bb', 'Barbados'), ('by', 'Belarus'), ('be', 'Belgium'), ('bz', 'Belize'), ('bj', 'Benin'), ('bt', 'Bhutan'), ('bo', 'Bolivia'), ('ba', 'Bosnia and Herzegovina'), ('bw', 'Botswana'), ('br', 'Brazil'), ('io', 'British Indian Ocean Territory'), ('bn', 'Brunei'), ('bg', 'Bulgaria'), ('bf', 'Burkina Faso'), ('bi', 'Burundi'), ('kh', 'Cambodia'), ('cm', 'Cameroon'), ('ca', 'Canada'), ('cv', 'Cape Verde'), ('bq', 'Caribbean Netherlands'), ('cf', 'Central African Republic'), ('td', 'Chad'), ('cl', 'Chile'), ('cn', 'China'), ('co', 'Colombia'), ('km', 'Comoros'), ('cd', 'Congo-Kinshasa'), ('cg', 'Congo-Brazzaville'), ('cr', 'Costa Rica'), ('ci', 'Côte d’Ivoire'), ('hr', 'Croatia'), ('cu', 'Cuba'), ('cw', 'Curaçao'), ('cy', 'Cyprus'), ('cz', 'Czech Republic'), ('dk', 'Denmark'), ('dj', 'Djibouti'), ('dm', 'Dominica'), ('do', 'Dominican Republic'), ('ec', 'Ecuador'), ('eg', 'Egypt'), ('sv', 'El Salvador'), ('gq', 'Equatorial Guinea'), ('er', 'Eritrea'), ('ee', 'Estonia'), ('et', 'Ethiopia'), ('fj', 'Fiji'), ('fi', 'Finland'), ('fr', 'France'), ('gf', 'French Guiana'), ('pf', 'French Polynesia'), ('ga', 'Gabon'), ('gm', 'Gambia'), ('ge', 'Georgia'), ('de', 'Germany'), ('gh', 'Ghana'), ('gr', 'Greece'), ('gd', 'Grenada'), ('gp', 'Guadeloupe'), ('gu', 'Guam'), ('gt', 'Guatemala'), ('gn', 'Guinea'), ('gw', 'Guinea-Bissau'), ('gy', 'Guyana'), ('ht', 'Haiti'), ('hn', 'Honduras'), ('hk', 'Hong Kong'), ('hu', 'Hungary'), ('is', 'Iceland'), ('in', 'India'), ('id', 'Indonesia'), ('ir', 'Iran'), ('iq', 'Iraq'), ('ie', 'Ireland'), ('il', 'Israel'), ('it', 'Italy'), ('jm', 'Jamaica'), ('jp', 'Japan'), ('jo', 'Jordan'), ('kz', 'Kazakhstan'), ('ke', 'Kenya'), ('ki', 'Kiribati'), ('xk', 'Kosovo'), ('kw', 'Kuwait'), ('kg', 'Kyrgyzstan'), ('la', 'Laos'), ('lv', 'Latvia'), ('lb', 'Lebanon'), ('ls', 'Lesotho'), ('lr', 'Liberia'), ('ly', 'Libya'), ('li', 'Liechtenstein'), ('lt', 'Lithuania'), ('lu', 'Luxembourg'), ('mo', 'Macau'), ('mk', 'Macedonia'), ('mg', 'Madagascar'), ('mw', 'Malawi'), ('my', 'Malaysia'), ('mv', 'Maldives'), ('ml', 'Mali'), ('mt', 'Malta'), ('mh', 'Marshall Islands'), ('mq', 'Martinique'), ('mr', 'Mauritania'), ('mu', 'Mauritius'), ('mx', 'Mexico'), ('fm', 'Micronesia'), ('md', 'Moldova'), ('mc', 'Monaco'), ('mn', 'Mongolia'), ('me', 'Montenegro'), ('ma', 'Morocco'), ('mz', 'Mozambique'), ('mm', 'Myanmar'), ('na', 'Namibia'), ('nr', 'Nauru'), ('np', 'Nepal'), ('nl', 'Netherlands'), ('nc', 'New Caledonia'), ('nz', 'New Zealand'), ('ni', 'Nicaragua'), ('ne', 'Niger'), ('ng', 'Nigeria'), ('kp', 'North Korea'), ('no', 'Norway'), ('om', 'Oman'), ('pk', 'Pakistan'), ('pw', 'Palau'), ('ps', 'Palestine'), ('pa', 'Panama'), ('pg', 'Papua New Guinea'), ('py', 'Paraguay'), ('pe', 'Peru'), ('ph', 'Philippines'), ('pl', 'Poland'), ('pt', 'Portugal'), ('pr', 'Puerto Rico'), ('qa', 'Qatar'), ('re', 'Réunion'), ('ro', 'Romania'), ('ru', 'Russia'), ('rw', 'Rwanda'), ('kn', 'Saint Kitts and Nevis'), ('lc', 'Saint Lucia'), ('vc', 'Saint Vincent and the Grenadines'), ('ws', 'Samoa'), ('sm', 'San Marino'), ('st', 'São Tomé and Príncipe'), ('sa', 'Saudi Arabia'), ('sn', 'Senegal'), ('rs', 'Serbia'), ('sc', 'Seychelles'), ('sl', 'Sierra Leone'), ('sg', 'Singapore'), ('sk', 'Slovakia'), ('si', 'Slovenia'), ('sb', 'Solomon Islands'), ('so', 'Somalia'), ('za', 'South Africa'), ('kr', 'South Korea'), ('ss', 'South Sudan'), ('es', 'Spain'), ('lk', 'Sri Lanka'), ('sd', 'Sudan'), ('sr', 'Suriname'), ('sz', 'Swaziland'), ('se', 'Sweden'), ('ch', 'Switzerland'), ('sy', 'Syria'), ('tw', 'Taiwan'), ('tj', 'Tajikistan'), ('tz', 'Tanzania'), ('th', 'Thailand'), ('tl', 'Timor-Leste'), ('tg', 'Togo'), ('to', 'Tonga'), ('tt', 'Trinidad and Tobago'), ('tn', 'Tunisia'), ('tr', 'Turkey'), ('tm', 'Turkmenistan'), ('tv', 'Tuvalu'), ('ug', 'Uganda'), ('ua', 'Ukraine'), ('ae', 'United Arab Emirates'), ('gb', 'United Kingdom'), ('us', 'United States'), ('uy', 'Uruguay'), ('uz', 'Uzbekistan'), ('vu', 'Vanuatu'), ('va', 'Vatican City'), ('ve', 'Venezuela'), ('vn', 'Vietnam'), ('ye', 'Yemen'), ('zm', 'Zambia'), ('zw', 'Zimbabwe')], db_index=True, max_length=255, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='agencyprofile',
            name='country_en',
            field=models.CharField(choices=[('af', 'Afghanistan'), ('al', 'Albania'), ('dz', 'Algeria'), ('ad', 'Andorra'), ('ao', 'Angola'), ('ag', 'Antigua and Barbuda'), ('ar', 'Argentina'), ('am', 'Armenia'), ('aw', 'Aruba'), ('au', 'Australia'), ('at', 'Austria'), ('az', 'Azerbaijan'), ('bs', 'Bahamas'), ('bh', 'Bahrain'), ('bd', 'Bangladesh'), ('bb', 'Barbados'), ('by', 'Belarus'), ('be', 'Belgium'), ('bz', 'Belize'), ('bj', 'Benin'), ('bt', 'Bhutan'), ('bo', 'Bolivia'), ('ba', 'Bosnia and Herzegovina'), ('bw', 'Botswana'), ('br', 'Brazil'), ('io', 'British Indian Ocean Territory'), ('bn', 'Brunei'), ('bg', 'Bulgaria'), ('bf', 'Burkina Faso'), ('bi', 'Burundi'), ('kh', 'Cambodia'), ('cm', 'Cameroon'), ('ca', 'Canada'), ('cv', 'Cape Verde'), ('bq', 'Caribbean Netherlands'), ('cf', 'Central African Republic'), ('td', 'Chad'), ('cl', 'Chile'), ('cn', 'China'), ('co', 'Colombia'), ('km', 'Comoros'), ('cd', 'Congo-Kinshasa'), ('cg', 'Congo-Brazzaville'), ('cr', 'Costa Rica'), ('ci', 'Côte d’Ivoire'), ('hr', 'Croatia'), ('cu', 'Cuba'), ('cw', 'Curaçao'), ('cy', 'Cyprus'), ('cz', 'Czech Republic'), ('dk', 'Denmark'), ('dj', 'Djibouti'), ('dm', 'Dominica'), ('do', 'Dominican Republic'), ('ec', 'Ecuador'), ('eg', 'Egypt'), ('sv', 'El Salvador'), ('gq', 'Equatorial Guinea'), ('er', 'Eritrea'), ('ee', 'Estonia'), ('et', 'Ethiopia'), ('fj', 'Fiji'), ('fi', 'Finland'), ('fr', 'France'), ('gf', 'French Guiana'), ('pf', 'French Polynesia'), ('ga', 'Gabon'), ('gm', 'Gambia'), ('ge', 'Georgia'), ('de', 'Germany'), ('gh', 'Ghana'), ('gr', 'Greece'), ('gd', 'Grenada'), ('gp', 'Guadeloupe'), ('gu', 'Guam'), ('gt', 'Guatemala'), ('gn', 'Guinea'), ('gw', 'Guinea-Bissau'), ('gy', 'Guyana'), ('ht', 'Haiti'), ('hn', 'Honduras'), ('hk', 'Hong Kong'), ('hu', 'Hungary'), ('is', 'Iceland'), ('in', 'India'), ('id', 'Indonesia'), ('ir', 'Iran'), ('iq', 'Iraq'), ('ie', 'Ireland'), ('il', 'Israel'), ('it', 'Italy'), ('jm', 'Jamaica'), ('jp', 'Japan'), ('jo', 'Jordan'), ('kz', 'Kazakhstan'), ('ke', 'Kenya'), ('ki', 'Kiribati'), ('xk', 'Kosovo'), ('kw', 'Kuwait'), ('kg', 'Kyrgyzstan'), ('la', 'Laos'), ('lv', 'Latvia'), ('lb', 'Lebanon'), ('ls', 'Lesotho'), ('lr', 'Liberia'), ('ly', 'Libya'), ('li', 'Liechtenstein'), ('lt', 'Lithuania'), ('lu', 'Luxembourg'), ('mo', 'Macau'), ('mk', 'Macedonia'), ('mg', 'Madagascar'), ('mw', 'Malawi'), ('my', 'Malaysia'), ('mv', 'Maldives'), ('ml', 'Mali'), ('mt', 'Malta'), ('mh', 'Marshall Islands'), ('mq', 'Martinique'), ('mr', 'Mauritania'), ('mu', 'Mauritius'), ('mx', 'Mexico'), ('fm', 'Micronesia'), ('md', 'Moldova'), ('mc', 'Monaco'), ('mn', 'Mongolia'), ('me', 'Montenegro'), ('ma', 'Morocco'), ('mz', 'Mozambique'), ('mm', 'Myanmar'), ('na', 'Namibia'), ('nr', 'Nauru'), ('np', 'Nepal'), ('nl', 'Netherlands'), ('nc', 'New Caledonia'), ('nz', 'New Zealand'), ('ni', 'Nicaragua'), ('ne', 'Niger'), ('ng', 'Nigeria'), ('kp', 'North Korea'), ('no', 'Norway'), ('om', 'Oman'), ('pk', 'Pakistan'), ('pw', 'Palau'), ('ps', 'Palestine'), ('pa', 'Panama'), ('pg', 'Papua New Guinea'), ('py', 'Paraguay'), ('pe', 'Peru'), ('ph', 'Philippines'), ('pl', 'Poland'), ('pt', 'Portugal'), ('pr', 'Puerto Rico'), ('qa', 'Qatar'), ('re', 'Réunion'), ('ro', 'Romania'), ('ru', 'Russia'), ('rw', 'Rwanda'), ('kn', 'Saint Kitts and Nevis'), ('lc', 'Saint Lucia'), ('vc', 'Saint Vincent and the Grenadines'), ('ws', 'Samoa'), ('sm', 'San Marino'), ('st', 'São Tomé and Príncipe'), ('sa', 'Saudi Arabia'), ('sn', 'Senegal'), ('rs', 'Serbia'), ('sc', 'Seychelles'), ('sl', 'Sierra Leone'), ('sg', 'Singapore'), ('sk', 'Slovakia'), ('si', 'Slovenia'), ('sb', 'Solomon Islands'), ('so', 'Somalia'), ('za', 'South Africa'), ('kr', 'South Korea'), ('ss', 'South Sudan'), ('es', 'Spain'), ('lk', 'Sri Lanka'), ('sd', 'Sudan'), ('sr', 'Suriname'), ('sz', 'Swaziland'), ('se', 'Sweden'), ('ch', 'Switzerland'), ('sy', 'Syria'), ('tw', 'Taiwan'), ('tj', 'Tajikistan'), ('tz', 'Tanzania'), ('th', 'Thailand'), ('tl', 'Timor-Leste'), ('tg', 'Togo'), ('to', 'Tonga'), ('tt', 'Trinidad and Tobago'), ('tn', 'Tunisia'), ('tr', 'Turkey'), ('tm', 'Turkmenistan'), ('tv', 'Tuvalu'), ('ug', 'Uganda'), ('ua', 'Ukraine'), ('ae', 'United Arab Emirates'), ('gb', 'United Kingdom'), ('us', 'United States'), ('uy', 'Uruguay'), ('uz', 'Uzbekistan'), ('vu', 'Vanuatu'), ('va', 'Vatican City'), ('ve', 'Venezuela'), ('vn', 'Vietnam'), ('ye', 'Yemen'), ('zm', 'Zambia'), ('zw', 'Zimbabwe')], db_index=True, max_length=255, null=True, verbose_name='Country'),
        ),
    ]
