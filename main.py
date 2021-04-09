import pickle
from web_scraping_utils import *
from gather_urls import gather_urls
from gather_study_data import gather_study_data
from filter_and_save_data import filter_and_save_data

def main():
    """---------------------------------"""
    """---------User Parameters---------"""
    """---------------------------------"""

    # ----- Set Stage of Script -----
    # 1: Get study URLs from search results
    # 2: Gather data from each study
    # 3: Filter and save data to CSV
    stage = 3

    # ----- stage = 1 -----
    search_range = True  # search over range of dates?
    start_date = ['03', '25', '2021']
    stop_date = ['03', '30', '2021']

    # ----- stage = 2 -----
    study_urls_file = '20210325_study_urls.pickle'

    # ----- stage = 3 -----
    study_data_file = '20210325_data.pickle'
    email_blacklist = ['.edu', '.gov', '@163.com', '@aber.ac.uk', 'clinical@', 'information@', 'info@', 'patients@', 'clinical.trial@',
                       '_info_clingov@', 'acertamc@', 'achillesfoothealthcentre@', 'actimab@', 'AD1trial@', 'ADEQUATE@',
                       'admin@', 'clinicaltrials@', 'registration@', 'benefit03@', 'cambridge@', 'cancer@', 'InnovationsMedical@', 'centra@', 'Clin_Ops@',
                       'clinica.fisio@', 'clinical_trial_coordinator@', 'clinical-operation@', 'clinical-trial@', 'clinical-trials_CTG@',
                       'clinical-trials-contact@', 'clinical-trials-disclosure@', 'clinical-trials@', 'clinical.info.jp@', 'clinical.science@',
                       'clinical.studies@', 'Clinical.Trials@', 'clinicalaffairs@', 'clinicaloperations@', 'clinicalresearch@', 'ClinicalResearch@',
                       'clinicalresearchteam@', 'clinicalstudies.meditec.sur@', 'Clinicalstudies@', 'clinicalstudy@', 'ClinicalTransparency@',
                       'clinicaltrial@', 'ClinicalTrial@', 'clinicaltrialdisclosure@', 'ClinicalTrialDisclosure@', 'clinicaltrialinquiry@',
                       'clinicaltrials.connect@', 'Clinicaltrials@', 'clinicaltrials011@', 'clinicaltrialscontactus@', 'clintriage.rdg@', 'Contact-US@',
                       'contact@', 'cstonera@', 'CT-Inquiries@', 'ctc.cipropal@', 'ctc.remit@', 'ctcvrc@', 'ctg@', 'ctgov@', 'ctihon@', 'CTRinfo@',
                       'ctsu.decrescendo@', 'CTUReferral@', 'DK0-Disclosure@', '_hotline@', 'eMediUSA@', 'eshmouncompany@', '_medinfo@', 'eurecart.1@',
                       '.gumypause@', 'ClinicalTrialsDisclosure@', 'global-roche-genentech-trials@', '_Clinical@', 'GS-US-334-1967@', 'ClinicalSupportHD@',
                       'info-trial@', 'information.center@', 'IR-CTRegistration@', 'JapanCS305@', 'JNJ.CT@', 'study@', 'medical.request@', 'medical@',
                       'medicalmonitor@', 'medinfo.USA@', 'MedInfo@', 'MedQueriesUS@', '.email@', 'office@', '.clinica@', 'pm.1@', '@stjude.org',
                       'regulatory@', 'referralinfo@', 'rehabilitation@', 'sanfilippo@', 'secretaria_tecnica@', 'painresearch@', 'study.losangeles@',
                       'studyinquiry@', 'inquiry@', 'sules@', 'CT.gov@', 'Volunteer.Leeds@', 'doctor@', 'medinfo@', 'clinicaltrialinfo@', 'research@',
                       'Research@', 'clinicaltrial_inquiries@', 'regulatory@','603enrolment@', 'rehabilitation@', 'clinical.trials@',
                       'Clinical.Trials@', 'ClinicalTrials@', 'information.center@', '2440LM-002study@', 'study-team@' ]
    sponsor_blacklist = ['University', 'Universidad','Universiti', 'Universitair', 'Universitari', 'Universit√†', 'Universitario',
                         'Universit√°rio', 'Universitas', 'Universitaria', 'Universit√§t', 'Universitaire', 'Unƒ±versity',
                         'University-Cerrahpasa', 'Universidad', 'Universit√†ria', 'Hospital', 'Hospitalier', 'HOSPITAL',
                         'Hospitals', 'Hopitaux', 'H√¥pital', 'H√©l√®ne', 'H√¥pitaux', 'Hospices', 'Healthcare', 'Community Health',
                         'Walter Reed', 'Military', 'Military Medicine', 'VA Office', 'Veterans', 'College', 'Colleges', 'School',
                         'Escola', 'Academy', 'Academisch', 'Agency','Education', 'Consortium', 'Polytechnique', 'Collaborative', 'Cooperative',
                         'Instructonal', 'Institution', 'Institute', 'Institutes', 'Institutet', 'Istituto', 'Institut', 'Clinical',
                         'Clinica', 'Clinics', 'Clinic', 'Clinique', 'Cliniques', 'Trials', 'Foundation', 'Fundacion', 'Pharmaceutica',
                         'Fundaci√≥n', 'Fundaci√≥', 'Funda√ß√£o', 'Fondazione', 'Federation', 'Faculdade', "Investigaci√≥n", 'contact', 
                         'Gruppo', 'Grupo', 'Groupe', 'Group', 'Obesity group', 'sponsor', 'County Council', 'Surgeons', 'Endo-Surgery',
                         'Surgery', 'Organisation for Research', 'Shepherd Center', 'Center of Endosurgery', 'Sangath', 'Medical Center', 'Medical Centre',
                         'Medical Service', 'Medical Organization', 'Medical Research', 'Research Center', 'Research Centre',
                         'Community Services', 'Health Alliance', 'Research Society', 'Research Institute', 'Research Clinical',
                         'Research Foundation', 'Medical Foundation', 'Research Network', 'Hematology Association', 'Medical Association',
                         'Cancer Association', 'French Association', 'Cancer Registry', 'Cardiovascular Association', 'Mental Health', 'Public Health',
                         'Food and Drug Administration (FDA)', 'Medical Sciences', 'Med Science', 'Medical Care', 'Health Authority', 'Rehabilitation Centre',
                         'Health Service', 'Health Services', 'Health Sciences', 'Eastern Health', 'Education Center', 'Centro', 'Centre', 'Center Trials',
                         'Heart Center', 'Health Center', 'Diabetes Center', 'Headache Center', 'Center Health',
                         'Centrum', 'German Center', 'Prevention Center', 'Fertility Center', 'Fertility Clinics', 'Cancer Center',
                         'Cancer Centre', 'Cancer Society', 'Surgery Center', 'Heart Initiative', 'Medical Affairs',
                         'Reproductive Medicine', 'Health System', 'Health Systems', 'Cardresearch', 'CardioFocus',
                         'Research Group', 'Oncology Group', 'Oncology Associates', 'Reseach Association','Society', 'Healthy Future',
                         'Health Decisions', 'Blood Center', 'Disorder', 'Disorders', 'Disease', 'Development', 'Exercise Program',
                         'Specialties', 'Disease Control', 'Rigshospitalet', 'Justin Arnall', 'Jiangsu Hansoh Pharmaceutical Co., Ltd.',
                         'Fondazione Santa Lucia', 'Region √ñrebro County', 'Pharmaceuticals', 'NHS Greater Glasgow and Clyde',
                         'Hongchang Guo', 'Hjalmar Bouma', 'Hongnan Mo', 'Hongxia Ma', 'Holterman, Ai-Xuan, M.D.', 'Holly Risdon',
                         'Holland', 'Holbaek Sygehus', 'Hoffman Oncology', 'Ho Young Hwang', 'Ho Sup Lee', 'Ho Sung Kim', 'Ho Kyung Seo',
                         'Italian Group', 'Hiroaki Sato, MD., PhD.', 'Herbert Lyerly', 'Henrik Wiggers', 'Henrik Lindman',
                         'Henrik Ditzel', 'Henriette Svarre Nielsen, MD, DMSc', 'Henning Bliddal', 'Henit Yanai', 'Hendrik Streeck',
                         'Hemovent GmbH',  'Helse Stavanger HF', 'Helse M√∏re og Romsdal HF', 'Helse Fonna', 'Help Therapeutics',
                         'Helmholtz Zentrum M√ºnchen ', 'Helio Tedesco Silva Junior', 'Helena DOMINGUEZ', 'Helen Reynolds', 'Helen Obilor',
                         'Helen Locke', 'Heinrich Schima', 'Heinrich Husslein', 'Heidi Ahonen', 'Hecheng Li M.D., Ph.D', 'Hebrew',
                         'Heart of England NHS Trust', 'He Huang', 'Hawaii Pacific Health', 'Hautklinik Darmstadt', 'Haute Ecole de Sant√© Vaud',
                         'Hatem AbuHashim', 'Harvard Pilgrim Health Care', 'Hartwig R. Siebner', 'Harpoon Therapeutics', 'Hannes Kortekangas',
                         'Hanna Savolainen-Peltonen', 'Hanna Kahila', 'Hanna Czajka', 'Kalos Medical', 'Hanane EL KENZ', 'Hanan Jafar', 'Han Yuan',
                         'Han weidong', 'Hamideh Sabbaghi', 'Hamad Medical Corporation', 'Halla Halldorsdottir', 'Haji', 'Hackensack Meridian Health',
                         'Haake', 'H. Tolga √áelik', 'H Scott Boswell', 'Gwendolyn Vuurberg', 'Guyguy K Tshima, MD', 'NHS Foundation Trust',
                         'Gustavo Reyes-Teran', 'Gustave Roussy, Cancer Campus, Grand Paris', 'Guohua Zeng', 'Gunther Meinlschmidt',
                         'GULIN FINDIKOGLU','Guizhi Du', 'Guillermo Ceniza Bordallo',
                         'GUILLEMIN Francis, MD', 'Guang Ning', 'GUALTIERO PALARETI', 'Grimshaw', 'Gregory A. Dekaban', 'Gregorio Covino',
                         'Gregor Berger', 'Greg Durm, MD', 'GREAT Network Italy', 'Great China Fatty Liver Consortium Limited',
                         'Grant Dorsey, M.D, Ph.D.', 'Graham Brown', 'Gorm Greisen', 'Goranka Radmiloviƒá',
                         'Goranka Radmiloviƒá', 'Goh Wen Yang', 'Gnankang Sarah Napoe', 'Global Healthy Living Foundation', 'Giuditta Benincasa',
                         'Giuliano Marchetti', 'Gkouskou Kalliopi', 'Glenn Bauman', 'Glenn-Milo Santos', 'Giammaria Fiorentini', 'Gianna Wilkie',
                         'Gilles Boire', 'Ginger Yang', 'Giovanni Mirabella', 'Gertrude J. Nieuwenhuijs-Moeke', 'Gi-Byoung Nam', 'Georgia Tsaousi',
                         'Gerencia de Atenci√≥n Primaria, Madrid', 'German Aortic Valve Registry', 'George T. Budd', 'Gena Ghearing',
                         'Gehad Abd Elaziz Mhmoud Ahmad', 'Gelb, Arthur F., M.D.', 'Ge Junbo', 'Ge Zheng', 'Geert D', 'Enseignement et la Recherche',
                         'GB002, Inc., a wholly owned subsidiary of Gossamer Bio, Inc.', 'Gary Alan Bass', 'Gary F. Rogers, MD', 'Gao', 'Garcia Calduch',
                         'Garcia, Jose M., MD, PhD', 'Gang Mar', 'Gaia AG', 'Galit Yogev-Seligmann', 'G√∂zel', 'G√ºnther Rezniczek', 'G√©rard Amarenco',
                         'G√©rond', 'G√∂ker Utku deƒüer', 'Future Genetics Limited', 'Future Medicine', 'Fu-Sheng Wang', 'Frida Hansson, MD',
                         'Frieda Wolf', 'Friedrich-Alexander-Universit√§t Erlangen-N√ºrnberg', 'FSV6, Ltd.', 'Red Cross', 'French Innovative Leukemia Organisation',
                         'Frede Donskov', 'Frederic Amant', 'Fran√ßois Lellouche', 'Francis Corazza', 'Francisco Andres de la Gala', 'Francisco Javier Navarro Moya',
                         'Francisco Unda Solano', 'Frank A. Bucci, Jr., M.D.', 'FRANK DECLAU', 'Frank Scharnowski', 'Fotona d.o.o.', 'for Myomectomy or Polymyomectomy',
                         'for Personalized Treatment', 'Fondazione Telethon', 'Florida Robotic Radiosurgery Association', 'Occupational Health', 'Filipa Malheiro',
                         'Fern√°ndez', 'Fernando L√≥pez Z√°rraga', 'Fernando Suarez Sipmann', 'Fedor', 'Felipe Atienza', 'Felix Chikita Fredy, MD',
                         'Felix Gutierrez', 'Felix Ratjen', 'Fatemeh Khakshoor', 'Father Flanagan', 'Fatih Demirkan, MD', 'Fatma Alzahraa Mohamed Ibrahim Hassan Haggag',
                         'FAUTER', 'Fauze Maluf Filho', 'FasciaFrance', 'Farmaceutici Damor Spa', 'Fan Weijun', 'Fang Wang', 'Fangfang Zeng', 'Faiza Gaba',
                         'Fabio Garofalo', 'F. Javier Martin Sanchez', 'Eyal Leibovitz', 'Evans Fernandez Perez', 'European Thoracic Oncology Platform',
                         'European LeukemiaNet', 'European Lung Cancer Working Party', 'European Myeloma Network', 'Europainclinics z.√∫.', 'Espen Lindholm',
                         'Esra KILIN√á AKMAN', 'Esra Tanrƒ±verdi', 'Esraa Hassan,MD', 'Esther Cubo', 'Esther Meijer', 'Estudios Cl√≠nicos Latino Am√©rica',
                         'ETH Zurich', 'Eric Albrecht', 'Eric Durand', 'Eric Hollander', 'Erich Seifritz', 'Erika Carmel ltd', 'Enrique Testa', 'Emilio Bouza',
                         'Emilio Ramos', 'Emily de los Reyes', 'Emma Hansson', 'Emma Marie Caroline Slack', 'Eldon Loh', 'Eleah Stringer',
                         'Elevation Myocardial Infarction', 'ELHARRAR Xavier', 'Elijah W. Stommel', 'Emanuela Keller', 'Emanuele Bosi', 'Emelie Malstam',
                         'Elaine Caldeira de Oliveira Guirro', 'Ehab Tarek Fahmy', 'Ehsan M saied', 'Eisai Limited', 'EJAVerheijen',
                         'Effective in Patients Receiving Chemotherapy', 'EDUARDO ALBENIZ', 'ECRI bv', 'Ebru ƒ∞nan Kƒ±rmƒ±zƒ±g√ºl',
                         'E. Peden, MD', 'Earle Burgess, MD', 'DynamiCare Health', 'Dumitru Casian', 'Duomed', 'Dufresne, Craig, MD, PC',
                         'Duk-Woo Park, MD', 'Drugs for Neglected Diseases', 'Dr Abdurrahman Yurtaslan Ankara Oncology Training and Research Hospital',
                         'Dr Afchine Fazel', 'Dr Andrew Stevens', 'Dr Carlo Lavalle', 'Dr Christophe LENCLUD', 'Dr Cipto Mangunkusumo General Hospital',
                         'Dr cliff Librach', 'Dr David DE BELS', 'Dr Fabrice BRUNEEL', 'Dr Georg Kranz', 'Dr Gerry Gin Wai Kwok', 'Dr Guillaume DUCHER',
                         'Dr John Kimoff', 'Dr Keir Lewis', 'Dr Lim Siu Min', 'Dr M. B. Breebaart', 'Dr Philippe CLEVENBERGH', 'Dr Rajendra A. Badwe',
                         'Dr Sze-Yuan Ooi', 'Dr Valerie ZELLER', 'Dr Vincent Misrai', 'Dr. Alberto Herreros de Tejada Echanoj√°uregui',
                         'Dr. Amy Latimer-Cheung, PhD', 'Dr. Anatoly Langer', 'Dr. Andreas Kammerlander', 'Dr. Andrew Baker', 'Dr. Andrew Lim',
                         'Dr. Anne Ellis', 'Dr. Anthony Ho', 'Dr. B. Catharine. Craven', 'Dr. Bertrand Lebouche', 'Dr. Chandran Medical Prof Corp',
                         'Dr. Christopher Bailey', 'Dr. D. Y. Patil Dental College & Hospital', 'Dr. Damian Redfearn', 'Dr. Damon Scales',
                         'Dr. Daniel P Morin, MD MPH FHRS', 'Dr. Danielle Vicus', 'Dr. David Maslove', 'Dr. David Spaner', 'Dr. Dean Reeves Clinic',
                         'Dr. Deneen Vojta', 'Dr. Diane Lougheed', 'Dr. Ekong E. Udoh', 'Dr. Eliza Hawkes', 'Dr. F. K√∂hler Chemie GmbH', 'Dr. Falk Pharma GmbH',
                         'Dr. Fareena Ghaffar', 'Dr. Frank Behrens', 'Dr. Giuseppe Fiorentino', 'Dr. Gordon Buduhan', 'Dr. Grace Parraga', 'Dr. Graham Wright',
                         'Dr. Grant M. Pagdin', 'Dr. Horst Schmidt Klinik GmbH', 'DR. JASSIM ALGHAITH', 'Dr. Jean-Francois Morin', 'Dr. Jean-Sebastien Delisle, MD, PhD',
                         'Dr. John Bartlett', 'Dr. Jurjan Aman', 'dr. Kaweh Mansouri', 'dr. Laura C. G. de Graaff-Herder', 'dr. M.J.N.L. Benders', 'Dr. Marcia Finlayson',
                         'Dr. Markus Alfred M√∂hlenbruch', 'Dr. med. Carlo Cereda', 'Dr. med. Hector Eloy Tamez Perez', 'Dr. med. Karsten Schenke', 'Dr. med. Katja Hatz',
                         'Dr. med. Mahir Karakas', 'Dr. Michael Esser', 'Dr. Najat Khalifa', 'Dr. Nayruz Knaana', 'Dr. Negrin University Hospital',
                         'Dr. Nyanda Elias Ntinginya', 'Dr. Osman Hospital', 'Dr. Paul Buderath', 'Dr. Pere Roura-Poch', 'Dr. Pradip Gyanwali,MD',
                         'Dr. R. Adhi Teguh Perma Iskandar, Sp.A(K)', 'Dr. Ronnie Shapira', 'Dr. Sam M. Wiseman', 'Dr. Sandra E Black', 'Dr. Sch√§r AG / SPA',
                         'Dr. Serge Thal', 'Dr. Siyami Ersek Thoracic and Cardiovascular Surgery Training and Research Hospital', 'Dr. Soetomo General Hospital',
                         'Dr. Sophie Degrauwe', 'dr. Stefano Nava', 'Dr. Stephen Choi', 'Dr. Struk Tetiana', 'Dr. Yaacov Lawrence', 'Dr. Zaineb Akram', 'dr.dargahi',
                         'Dr.Jhuma Biswas', 'Dr.L√ºtfi Kƒ±rdar Kartal Eƒüitim ve Ara≈ütƒ±rma Hastanesi', 'Dr.Laurent Mineur', 'Dr.Pankaj Chaturvedi',
                         'Dr√§gerwerk AG & Co. KGaA', 'Douglas B. Sawyer', 'Douglas Boreham', 'Douglas Fraser', 'Doo-Sik Kong', 'Dorit Pud', 'Dorte Nielsen',
                         'Dong-Xin Wang', 'Dominik Abt', 'Dominik Ettlin', 'Dominik Glinz', 'Dominque Bullens', 'Donation', 'Donato F Altomare', 'Dong Jun Lim',
                         'Dong Wang', 'Dong Yang', 'Dissou AFFOLABI', 'Ditte Hansen', 'DKMS gemeinn√ºtzige GmbH', 'Do-Yoon Kang', 'Do-Youn Oh', 'doaa rashwan',
                         'Doctor Giacomo Gastaldi', 'Doctors with Africa - CUAMM', 'DILEK SAYIK', 'Dimitri Christoforidis', 'Dinara Zhumanbayeva', 'Ding Ma',
                         'Dipan Shah', 'Direction Centrale du Service de Sant√© des Arm√©es', 'Diameter', 'Diana Zach', 'DiGasparro', 'DEYGAS', 'Di Deng',
                         'Deutsches Herzzentrum Muenchen', 'Devan Parrott', 'Deok-Hwan Yang', 'Dennis Bregner Zetner', 'Dennis Jensen, Ph.D.',
                         'Dentali', 'Dean Nakamoto', 'Deborah O', 'Debra Friedman', 'Debra Weese-Mayer', 'Decathlon SE', 'Deepa Jagadeesh',
                         'Deepak Kilari', 'DatAids', 'David Bajor', 'David Baskin MD', 'David Brunk', 'David Cave', 'David Clarke', 'David D', 'David Drobne',
                         'David Filgueiras-Rama', 'David Garcia Cinca', 'David Gomez Almaguer', 'David Grant U.S. Air Force Medical Center', 'David H. Canaday',
                         'David Haines, MD', 'David J. Kopsky', 'David Lunardini', 'David Minor, MD', 'David Morris', 'David Nichols, MD', 'David Nichols, MD',
                         'David P. Kuwayama', 'David Palma', 'David Peran', 'David Scheiner', 'David Suskind', 'David True', 'David VanderWeele', 'David Wald',
                         'Davide Di Santo', 'Davide La Regina', 'Darwin Ang', 'Daren K. Heyland', 'Dario Sorrentino', 'Dario Valcarenghi', 'Darrell Tan',
                         'Abeona Therapeutics, Inc', 'ABEYE', 'Abliva AB', 'Abraham Reichenberg', 'AC Immune SA', 'Acceleron Pharma Inc.', 'Acerta Pharma BV',
                         'Achilles Therapeutics UK Limited', 'Actelion', 'Ad scientiam', 'Adam Bataineh', 'Adaptimmune', 'Adaptive Health, Inc',
                         'ADC Therapeutics S.A.', 'Aditya Kaza', 'Aditya S. Pandey, MD', 'Adocia', 'Adrian Vella', 'Adrianna Vlachos',
                         'Advanced Accelerator Applications', 'AgelessRx', 'AHS Cancer Control Alberta', 'Alaa Hassan M. Elhawary', 'Andreas R√ºck',
                         'Anna Martling', 'Annapoorna Kini', 'Arkin', 'Ascension South East Michigan', 'Asir John Samuel', 'Atridia Pty Ltd.', 'AZ Delta',
                         'AZ Sint-Jan AV', 'AZ-VUB', 'Azidus Brasil', 'Azienda di Servizi alla Persona di Pavia', 'Azienda Ospedaliera',
                         'Azienda Ospedaliera Citt√† della Salute e della Scienza di Torino', 'Azienda Ospedaliera di Padova',
                         'Azienda Ospedaliera Ospedale Infantile Regina Margherita', 'Azienda Ospedaliera San Giovanni Battista', 'Azienda Policlinico Umberto I',
                         'Azienda Sanitaria di Firenze', 'Azienda Sanitaria Locale Napoli 2 Nord', 'Azienda Socio Sanitaria Territoriale degli Spedali Civili di Brescia',
                         'Azienda Socio Sanitaria Territoriale del Garda', 'Azienda ULSS 3 Serenissima', 'Azienda Unit√† Sanitaria Locale di Piacenza',
                         'Azienda Unit√† Sanitaria Locale di Piacenza', 'Azienda Unit√† Sanitaria Locale Reggio Emilia', 'Azienda Unit√† Sanitaria Locale Reggio Emilia',
                         'Azienda Usl di Bologna', 'Azienda Usl di Bologna', 'Azienda USL Modena', 'Azienda USL Toscana Centro', 'Azienda USL Toscana Nord Ovest',
                         'Aziende Chimiche Riunite Angelini Francesco S.p.A', 'Bai Chunxue', 'Baptist Health South Florida', 'Barbara Ensoli, MD, PhD',
                         'Baxalta now part of Shire', 'Beijing Duheng for Drug Evaluation and Research Co., Ltd. (DDER)', 'Beijing InnoCare Pharma Tech Co., Ltd.',
                         'BENISTY', 'Bin He', 'Bjarne Linde Noergaard', 'Bjorn H. Ebdrup', 'Bon-Kwon Koo', 'CalciMedica, Inc.', 'Cancer Trials Ireland',
                         'Cancer Vaccines Limited', 'Cankado Service GmbH', 'Carcinoma', 'Catholic Relief Services', 'CCRF Inc., Beijing, China', 'CCTU- Cancer Theme',
                         'Celso Arango, MD, PhD', 'Cem Demirel', 'Center Eugene Marquis', 'Center for Epidemiology and Health Research, Germany',
                         'Center for Eye Research Australia', 'Center for Human Reproduction', 'Center for Information and Counseling on Reproductive Health - Tanadgoma',
                         'Center for Integrated Care', 'Center for International Blood and Marrow Transplant Research', 'Center For Interventional Pain and Spine',
                         'Center for Sight, Sacramento, CA', 'Center for Vaccine Development - Mali', 'Center of Integrative Addiction Research, Austria',
                         'Center of Personalized Medicine, Pirogova', 'Cerebral Palsy Greece - Open Door', 'CETERA', 'Ch Mont de Marsan', 'Chang-Qing Gao',
                         'Change Accelerator in Respiratory Care', 'Chiesi SA/NV', 'Chiesi UK', 'Childhood Development', 'Aid Society in Clearfield County',
                         'Healthcare of Atlanta', 'Christian Candrian', 'Christian Meier', 'CHU de Reims', 'Ciim Plus, d.o.o.', '√éle de Montr√©al',
                         'ClarData', 'Claudia Aristiz√°bal', 'Claudio Gobbi', 'ClinAmygate', 'CMC Ambroise Par√©', 'CMN "20 de Noviembre"',
                         'CNAO National Center of Oncological Hadrontherapy', 'CNGE IRMG Association', 'Collabree AG', 'Collegium Medicum w Bydgoszczy',
                         'Commonwealth Scientific and Industrial Research Organisation, Australia', 'Community Medical Center, Toms River, NJ',
                         'Community Memorial Health System', 'COMPASS Pathways', 'ConMed Linvatec Beijing', 'Coordinator', 'Cornea Associates of Texas',
                         'Corporacion Parc Tauli', 'Corporeal Circulation', 'CORTESI LAURA', 'Craig Anderson', 'CRG UZ Brussel', 'Cristina Avenda√±o Sol√°',
                         'Cristina Martinez', 'Croydon Health Services NHS Trust', 'Crozer-Keystone Health System', 'CT.gov Call Center', 'Cui Yimin', 'Da Fu',
                         'Da, Yuwei, M.D.', 'Dafne Balemans', 'Daiichi Sankyo Turkey, a Daiichi Sankyo Company', 'Dairy Goat Co-operative (N.Z.) Limited',
                         'Dalarna County Council, Sweden', 'Damian Ratano', 'Dan Adler', 'Dan Rhon', 'Dan Su', 'Dan Zandberg', 'Danbury Hospital', 'Daniel Claassen',
                         'Daniel L Lustgarten', 'Daniela Francescato Veiga', 'Daniela Nosch', 'Danielle Gentile', 'Danilo Toni', 'Danisco' ]

                       

    """---------------------------------"""
    """---------------------------------"""
    """---------------------------------"""

    """Read Data from Skipped Stages"""
    if stage == 2:
        with open(study_urls_file, "rb") as handle:
            study_urls = pickle.load(handle)
        print("Successfully read study urls from: ", study_urls_file)
    elif stage == 3:
        with open(study_data_file, "rb") as handle:
            data = pickle.load(handle)
        print("Successfully read study data from: ", study_data_file)

    """Execute Each Stage"""
    if stage == 1:
        """Gather URLs of each study in the search results"""
        print("Stage 1:")
        if search_range:
            print("\tSearching studies updated between:", start_date, "-", stop_date)
        else:
            print("\tSearching all studies in database")
        study_urls = gather_urls(search_range, start_date, stop_date)
        stage += 1
    if stage == 2:
        """Gather Study Information"""
        print("Stage 2:")
        print("\tGathering data from each study")
        data = gather_study_data(study_urls)
        stage += 1
    if stage == 3:
        """Filter and save data to CSV"""
        print("Stage 3:")
        print("\tFiltering data and saving to CSV")
        filter_and_save_data(data, email_blacklist, sponsor_blacklist)


if __name__ == "__main__":
    main()
