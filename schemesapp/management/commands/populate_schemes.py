from django.core.management.base import BaseCommand
from schemesapp.models import Scheme


class Command(BaseCommand):
    help = 'Populate database with Sikkim government schemes'

    def handle(self, *args, **options):
        schemes_data = [
            # Education Schemes
            {
                'name': 'Sikkim Scholarship for Meritorious Students',
                'objective': 'Provide financial assistance to meritorious students from Sikkim',
                'benefits': 'Monthly stipend of ₹500-1000 + Educational materials',
                'agency': 'Department of Education',
                'category': 'education',
                'full_description': 'Financial assistance program for students scoring above 75% in Class XII exams from recognized institutions in Sikkim.',
                'contact_email': 'education@sikkim.gov.in',
                'contact_phone': '+91-3592-205555',
                'min_age': 14,
                'max_age': 25,
            },
            {
                'name': 'Sikkim Higher Education Scholarship',
                'objective': 'Support higher education for economically weaker sections',
                'benefits': 'Upto ₹2,00,000 per annum for college/university fees',
                'agency': 'Department of Human Resources Development',
                'category': 'education',
                'full_description': 'Scholarship for students from economically weaker families pursuing graduation or postgraduate courses.',
                'min_age': 18,
                'max_age': 30,
                'below_poverty_line': True,
            },
            {
                'name': 'Free Vocational Training Programme',
                'objective': 'Provide skill development through vocational training',
                'benefits': 'Free training in various trades + Certificate',
                'agency': 'Department of Skill Development',
                'category': 'education',
                'full_description': 'Free vocational training in trades like electrician, plumbing, carpentry, and welding.',
                'contact_phone': '+91-3592-208999',
                'min_age': 16,
                'max_age': 45,
            },

            # Health Schemes
            {
                'name': 'Sikkim Health Insurance Scheme',
                'objective': 'Provide universal health coverage to all citizens',
                'benefits': 'Cashless treatment up to ₹5,00,000 in empanelled hospitals',
                'agency': 'Department of Health',
                'category': 'health',
                'full_description': 'Comprehensive health insurance coverage for all residents of Sikkim including hospitalization, surgery, and diagnostics.',
                'contact_email': 'health@sikkim.gov.in',
            },
            {
                'name': 'Maternal and Child Health Scheme',
                'objective': 'Reduce maternal and infant mortality rates',
                'benefits': 'Free antenatal care, delivery, postnatal care + Cash assistance',
                'agency': 'Department of Health',
                'category': 'health',
                'full_description': 'Complete maternal and child health support including regular check-ups, delivery assistance, and postpartum care.',
                'gender': 'F',
            },
            {
                'name': 'Disability Rehabilitation and Support',
                'objective': 'Support persons with disabilities',
                'benefits': 'Monthly assistance ₹500-2000 + Free medical aids and equipment',
                'agency': 'Department of Social Justice',
                'category': 'health',
                'full_description': 'Financial assistance and medical equipment support for persons with disabilities.',
                'disability': True,
            },

            # Agriculture Schemes
            {
                'name': 'Sikkim Organic Farming Subsidy',
                'objective': 'Promote organic farming in Sikkim',
                'benefits': '50% subsidy on organic seeds, fertilizers and tools',
                'agency': 'Department of Agriculture',
                'category': 'agriculture',
                'full_description': 'Financial assistance to farmers for transitioning to organic farming practices.',
                'contact_email': 'agriculture@sikkim.gov.in',
                'location': 'rural',
            },
            {
                'name': 'Kisan Credit Card Scheme',
                'objective': 'Provide credit for agricultural needs',
                'benefits': 'Easy credit facility up to ₹1,00,000 at 4% interest',
                'agency': 'Department of Agriculture & Allied Services',
                'category': 'agriculture',
                'full_description': 'Credit facility for farmers to meet their short-term and medium-term agricultural credit needs.',
                'location': 'rural',
            },
            {
                'name': 'Agricultural Mechanization Scheme',
                'objective': 'Provide modern farm machinery support',
                'benefits': '40-50% subsidy on agricultural machinery',
                'agency': 'Department of Agriculture',
                'category': 'agriculture',
                'full_description': 'Subsidy on purchase of modern agricultural machinery for farms.',
                'contact_phone': '+91-3592-206666',
                'location': 'rural',
            },

            # Business & Employment
            {
                'name': 'Sikkim Startup Employment Scheme',
                'objective': 'Encourage entrepreneurship and job creation',
                'benefits': 'Upto ₹10,00,000 loan at 3% interest + Mentorship',
                'agency': 'Department of Industries',
                'category': 'business',
                'full_description': 'Financial support and business guidance for aspiring entrepreneurs starting their own ventures.',
                'contact_email': 'industries@sikkim.gov.in',
                'min_age': 18,
                'max_age': 40,
            },
            {
                'name': 'PMEGP - Micro Enterprises Scheme',
                'objective': 'Promote micro and small enterprises',
                'benefits': 'Subsidy up to ₹25,00,000 on project cost + Training',
                'agency': 'Department of MSME',
                'category': 'business',
                'full_description': 'Subsidy and credit facility for setting up micro enterprises in manufacturing and services sectors.',
                'min_age': 18,
            },
            {
                'name': 'Youth Employment Generation Scheme',
                'objective': 'Create employment opportunities for youth',
                'benefits': '₹5000-10000 monthly stipend for 6-12 months',
                'agency': 'Department of Labor',
                'category': 'employment',
                'full_description': 'Employment subsidy program for unemployed youth to gain work experience and skills.',
                'min_age': 18,
                'max_age': 35,
            },

            # Social Welfare
            {
                'name': 'Old Age Pension Scheme',
                'objective': 'Provide financial assistance to senior citizens',
                'benefits': 'Monthly pension ₹2000-4000',
                'agency': 'Department of Social Justice',
                'category': 'social',
                'full_description': 'Regular monthly pension for citizens aged 60 years and above.',
                'contact_phone': '+91-3592-207777',
                'min_age': 60,
            },
            {
                'name': 'Widow Pension Scheme',
                'objective': 'Support widows and provide social security',
                'benefits': 'Monthly pension ₹1500-2500',
                'agency': 'Department of Social Justice',
                'category': 'social',
                'maritial_status': 'WIDOWED',
                'gender': 'F',
            },
            {
                'name': 'BPL Food Grain Scheme',
                'objective': 'Provide food security to poor families',
                'benefits': '35 kg rice/wheat monthly at subsidized rates',
                'agency': 'Department of Food & Public Distribution',
                'category': 'social',
                'full_description': 'Subsidized food grains for families below the poverty line.',
                'below_poverty_line': True,
            },

            # Women Empowerment
            {
                'name': 'Sikkim Women Self Help Group Scheme',
                'objective': 'Empower women through group activities',
                'benefits': '₹5,00,000 group loan at 3% interest + Training',
                'agency': 'Department of Rural Development',
                'category': 'women',
                'full_description': 'Financial support and training for women self-help groups engaged in productive activities.',
                'gender': 'F',
            },
            {
                'name': 'Mahila Shakti Yojana',
                'objective': 'Economic and social empowerment of women',
                'benefits': 'Microfinance upto ₹2,00,000 + Skill training',
                'agency': 'Ministry of Women and Child Development',
                'category': 'women',
                'full_description': 'Comprehensive program for women entrepreneurship and skill development.',
                'contact_email': 'women@sikkim.gov.in',
                'gender': 'F',
                'min_age': 18,
                'max_age': 55,
            },
            {
                'name': 'Beti Bachao Beti Padhao Scheme',
                'objective': 'Support education of girl child',
                'benefits': '₹1000 annually till completion of Class XII',
                'agency': 'Department of Education',
                'category': 'women',
                'full_description': 'Educational support and incentives for girl children from economically weaker families.',
                'gender': 'F',
            },

            # Infrastructure & Housing
            {
                'name': 'Pradhan Mantri Awas Yojana',
                'objective': 'Provide affordable housing to all',
                'benefits': 'Housing subsidy upto ₹2,30,000',
                'agency': 'Ministry of Housing & Urban Affairs',
                'category': 'infrastructure',
                'full_description': 'Affordable housing scheme for economically weaker sections and low-income groups.',
                'contact_phone': '+91-3592-209999',
                'below_poverty_line': True,
            },

            # Sports & Recreation
            {
                'name': 'Sports Talent Development Scheme',
                'objective': 'Support young sports talent',
                'benefits': 'Monthly stipend ₹1500-5000 + Training support',
                'agency': 'Department of Sports & Youth Affairs',
                'category': 'sports',
                'full_description': 'Financial support and training for identified sports talents.',
                'min_age': 12,
                'max_age': 25,
            },
            {
                'name': 'Sikkim Youth Development Programme',
                'objective': 'Holistic development of youth',
                'benefits': 'Leadership training + Sports facilities + Internships',
                'agency': 'Department of Youth Affairs',
                'category': 'sports',
                'full_description': 'Comprehensive youth development program including sports, skills, and leadership training.',
                'min_age': 18,
                'max_age': 30,
            },

            # Other Important Schemes
            {
                'name': 'SC/ST/OBC Special Scholarship',
                'objective': 'Support backward caste students',
                'benefits': 'Monthly scholarship ₹500-1500 + Career guidance',
                'agency': 'Department of Social Justice',
                'category': 'social',
                'full_description': 'Special scholarship for students from SC/ST/OBC communities.',
                'caste': 'SC',
            },
            {
                'name': 'Minority Welfare Scholarship',
                'objective': 'Educational support for minorities',
                'benefits': 'Scholarship covering 50-100% of tuition fees',
                'agency': 'Department of Minority Affairs',
                'category': 'education',
                'full_description': 'Scholarship scheme for students from minority communities.',
                'minority': True,
            },
            {
                'name': 'Skill India Mission',
                'objective': 'Skill development across sectors',
                'benefits': 'Free skill training + Job placement assistance',
                'agency': 'Ministry of Skill Development',
                'category': 'employment',
                'full_description': 'Comprehensive skill development program with job placement support.',
                'min_age': 16,
                'max_age': 40,
            },
            {
                'name': 'Jan Dhan Yojana',
                'objective': 'Financial inclusion for all citizens',
                'benefits': 'Free bank account + Accident insurance ₹1,00,000',
                'agency': 'Department of Finance',
                'category': 'other',
                'full_description': 'Universal bank account access for financial inclusion and security.',
                'contact_email': 'finance@sikkim.gov.in',
            },
            {
                'name': 'Ayushman Bharat Health Scheme',
                'objective': 'Universal health coverage initiative',
                'benefits': 'Free hospitalization upto ₹5,00,000 annually',
                'agency': 'Ministry of Health & Family Welfare',
                'category': 'health',
                'full_description': 'National health protection scheme providing free treatment in empanelled hospitals.',
                'contact_phone': '+91-3592-208888',
                'below_poverty_line': True,
            },
            {
                'name': 'Rashtriya Swasthya Bima Yojana',
                'objective': 'Health protection for unorganized sector workers',
                'benefits': 'Health insurance coverage ₹30,000 per family annually',
                'agency': 'Ministry of Labor & Employment',
                'category': 'health',
                'full_description': 'Health insurance scheme for unorganized sector workers and their dependents.',
            },
        ]

        created_count = 0
        for scheme_data in schemes_data:
            try:
                scheme, created = Scheme.objects.get_or_create(
                    name=scheme_data['name'],
                    defaults=scheme_data
                )
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[+] Created: {scheme.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'[~] Already exists: {scheme.name}')
                    )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'[X] Error creating {scheme_data["name"]}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n[+] Total schemes created: {created_count}')
        )
