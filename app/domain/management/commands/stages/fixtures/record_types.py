"""Record types."""

RECORD_TYPE_COVERSIONS = {
    'Account Book-Other': 'Account Book',
    'Liquidation of guardianship': 'Guardianship-Liquidation',
    'Failed Seizure': 'Seizure-Failed',
    'Testamentary execution': 'Testament-Execution',
    'Object List-Fictional': 'Fictional object list',
    'unclear': 'Unclear',
    'Dowry': 'Inventory-Dowry',
}

RECORD_TYPES = {
    'DALME': [
        {
            'name': 'Inventory',
            'subtypes': [
                'Comanda',
                'Confiscation',
                'Criminal Inquest',
                'Custody',
                'Division',
                'Donation',
                'Dowry',
                'Dowry Restitution',
                'Ecclesiastical',
                'Emancipation',
                'Generic',
                'Guardianship',
                'Insolvency',
                'Legacy',
                'List of objects',
                'Postmortem',
                'Premortem',
                'Probate',
                'Quittance',
                'Repudiation of inheritance',
                'Restitution of pawned goods',
                'Ship',
                'Taking up inheritance',
                'Tax seizure',
                'Tax assessment',
                'Undefended Goods',
            ],
        },
        {
            'name': 'Account Book',
            'subtypes': [
                'Household',
                'Commercial',
                'Ecclesiastical',
            ],
        },
        {
            'name': 'Guardianship',
            'subtypes': [
                'Liquidation',
            ],
        },
        {
            'name': 'Seizure',
            'subtypes': [
                'Failed',
                'Debt',
                'Confiscation',
            ],
        },
        {
            'name': 'Testament',
            'subtypes': [
                'Execution',
            ],
        },
        {
            'name': 'Sale',
            'subtypes': [
                'Auction',
                'Notarial',
                'Account',
            ],
        },
        {
            'name': 'Estimate',
            'subtypes': [
                'Dowry',
                'Testament',
                'Insolvency',
                'Pledge',
                'Investment',
                'Theft',
            ],
        },
        {
            'name': 'Tariffs',
            'subtypes': [
                'Price Caps',
                'Lists',
                'Customs Registers',
            ],
        },
        {
            'name': 'Arrest',
            'subtypes': None,
        },
        {
            'name': 'Auction',
            'subtypes': None,
        },
        {
            'name': 'Codicil',
            'subtypes': None,
        },
        {
            'name': 'Eviction',
            'subtypes': None,
        },
        {
            'name': 'Incarceration',
            'subtypes': None,
        },
        {
            'name': 'Fictional object list',
            'subtypes': None,
        },
        {
            'name': 'Order to deliver goods',
            'subtypes': None,
        },
        {
            'name': 'Promise to pay debt',
            'subtypes': None,
        },
        {
            'name': 'Renvoi',
            'subtypes': None,
        },
        {
            'name': 'Unclear',
            'subtypes': None,
        },
    ],
    'Pharmacopeias': [
        {
            'name': 'Pharmacopeia',
            'subtypes': [
                'Functional',
                'Reference',
            ],
        },
    ],
}
