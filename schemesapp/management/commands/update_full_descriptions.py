from django.core.management.base import BaseCommand
from schemesapp.models import Scheme

class Command(BaseCommand):
    help = 'Update full_description field for Scheme model based on predefined data.'

    def handle(self, *args, **options):
        data = {
            "Chief Minister's State Disability Pension Scheme": "This scheme provides a monthly pension of ₹1,500 to individuals with 40% or more disability in Sikkim. Implemented by the Women & Child Welfare Department, it aims to offer financial assistance to differently-abled persons without any age restrictions. The scheme is entirely state-funded and is part of Sikkim's commitment to supporting its disabled population.",
            "Comprehensive Educational Loan Scheme": "CELS offers interest-free loans to students pursuing higher education, both within India and abroad. The scheme includes a one-year moratorium period after course completion. Special consideration is given to students from Below Poverty Line (BPL) families and those enrolled in professional courses. Loan amounts can go up to ₹15 lakh for studies abroad.",
            "Chief Minister's Self Employment Scheme": "CMSES provides financial assistance up to ₹3 lakh to unemployed youth aged between 22 and 35 years who have passed at least the 10th grade. Applicants must come from families with an annual income not exceeding ₹2.5 lakh. The scheme encourages self-employment and entrepreneurship among the youth of Sikkim.",
            "Pension Benefit for the Construction Worker": "This scheme offers a monthly pension of ₹10,000 to registered construction workers in Sikkim upon reaching the age of 60. It ensures financial security and recognizes the contributions of long-serving workers in the construction sector.",
            "Chief Ministers’ Education Assistance Scheme": "CMEAS aims to provide financial assistance to students from economically weaker sections, marginalized communities, and specially-abled students. The scheme supports these students in pursuing higher education by alleviating financial burdens.",
            "Sikkim Grant Of Award To Transgender (SGATT)": "Under the Sikkim Payment of Grant to the Transgender Rules 2013, this scheme provides financial grants to transgender individuals. It aims to support their welfare and integration into society by offering monetary assistance.",
            "Indira Gandhi National Widow Pension Scheme (IGNWPS)": "IGNWPS is a centrally sponsored scheme that provides a monthly pension of ₹2,000 to widows from BPL households in Sikkim. The scheme offers social security and financial support to widowed women, helping them meet their basic needs.",
            "Permanent Disability/ Death Benefit for the Construction Workers": "This welfare scheme provides financial assistance of ₹1.5 lakh to the nominees or dependents of registered construction workers in case of death or permanent disability. It aims to offer financial security to the families of workers affected by unforeseen circumstances.",
            "Su-Swastha Yojana": "Su-Swastha Yojana is a health service scheme for government employees of Sikkim and their dependent family members. It offers cashless hospitalization benefits across top-tier hospitals in India, ensuring comprehensive healthcare coverage for beneficiaries.",
            "Mission for Integrated Development of Horticulture (MIDH)": "MIDH is a centrally sponsored scheme aimed at the holistic growth of the horticulture sector in Sikkim. It covers the development of fruits, vegetables, root and tuber crops, mushrooms, spices, and more, promoting sustainable horticultural practices.",
            "Rashtriya Krishi Vikas Yojana (RKVY)": "RKVY is an initiative to boost agricultural development in Sikkim. It provides subsidies ranging from 20% to 50% for cultivating fruits and traditional farming, aiming to enhance farmers' income and promote sustainable agriculture.",
            "Chief Minister’s Free Scholarship Scheme (CMFSS)": "CMFSS offers scholarships to students from economically weaker sections in Sikkim. The scheme aims to support meritorious students in pursuing higher education without financial constraints.",
            "Board of Open Schooling and Skill Education (BOSSE)": "BOSSE is a state open school board in Sikkim that provides opportunities for secondary and senior secondary education, as well as skill and vocational training. It caters to students who have missed formal schooling, enabling them to continue their education.",
            "Chief Minister’s Annual and Total Health Checkup (CATCH)": "CATCH is a health initiative that provides comprehensive annual and periodic health check-ups to all citizens of Sikkim. The program aims to detect health issues early and maintain a health database for preventive healthcare.",
            "Mukhya Mantri Jeevan Raksha Kosh": "MMJRK is a health assistance fund for economically weaker sections in Sikkim. It provides financial aid for medical treatments, especially for those referred for treatment outside the state, ensuring access to necessary healthcare services.",
            "Chief Minister Rural Housing Scheme": "This scheme focuses on providing housing to rural populations in Sikkim. It aims to improve living conditions by constructing durable and affordable houses for families in need.",
            "Sikkim Garib Awas Yojana (SGAY)": "SGAY is a housing scheme targeting economically disadvantaged families in Sikkim. It provides financial assistance for the construction of houses, aiming to eliminate homelessness and improve living standards.",
            "Chief Minister’s Startup Scheme (CMSS)": "CMSS encourages entrepreneurship among the youth of Sikkim by providing financial support to start new ventures. The scheme offers assistance to individuals aged 15 to 40 years, promoting self-employment and economic development."
        }

        for name, full_desc in data.items():
            schemes = Scheme.objects.filter(name=name)
            if schemes.exists():
                for scheme in schemes:
                    scheme.full_description = full_desc
                    scheme.save()
                self.stdout.write(self.style.SUCCESS(f"Updated {schemes.count()} entries for '{name}'"))
            else:
                self.stdout.write(self.style.WARNING(f"No scheme found with name '{name}'"))