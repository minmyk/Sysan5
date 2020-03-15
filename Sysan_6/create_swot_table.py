import pandas as pd


def deambiguos(array, letter):
    indexes = list(map(lambda index: letter + str(index + 1), range(len(array))))
    return indexes


class Parasha:
    def __init__(self):
        self.strengths = (
            "No human interaction in driving",
            "Prevention of car accidents",
            "Speed limit",
            "Traffic analysis and lane moving control",
            "ABS, ESP systems",
            "Automatic Parking",
            "Fully automated Traffic Regulations",
            "Rational route selection",
            "Rational fuel usage",
            "Public transport sync",
            "Automatic photos",
            "Rational time management",
                     )
        self.weaknesses = (
            "System wear",
            "Huge computational complexity",
            "Electric dependency",
            "Computer vision weaknesses (accuracy)",
            "Huge error price",
            "Potential persnal data leakage",
            "GPS/Internet quality",
            "No relationships with non-automated cars",
            "Trolley problem",
            "Software bugs",
            "High price",
            "Man depends on vehicle"
                      )
        self.opportunities = (
            "E-maps of road signs",
            "Vehicle to vehicle connection",
            "More passanger places (no driver needed)",
            "System to prevent trafic jams",
            "Alternative energy usage",
            "New powerful computer vision technologies",
            "Cars technologies with less polution",
            "High efficency engines",
            "High demand on cars",
            "Goverment support of autonomous cars dev",
                         )

        self.threats = (
            "High production price",
            "High service price",
            "Not enough qualified mechanics",
            "Bad road cover surface",
            "Not ordinary behaivor of some road users",
            "Rejection by people",
            "Hacking, confidentiality problems",
            "Increased scam interest",
            "Job abolition",
            "Inadequacy of legal system",
                   )
        self.so_letters = None
        self.st_letters = None
        self.wo_letters = None
        self.wt_letters = None
        
    def parasha(self):
        strengths_letters = deambiguos(self.strengths, 'S')
        weaknesses_letters = deambiguos(self.weaknesses, 'W')
        opportunities_letters = deambiguos(self.opportunities, 'O')
        threats_letters = deambiguos(self.threats, 'T')

        st = pd.DataFrame(index=self.strengths, columns=self.threats)
        so = pd.DataFrame(index=self.strengths, columns=self.opportunities)
        wt = pd.DataFrame(index=self.weaknesses, columns=self.threats)
        wo = pd.DataFrame(index=self.weaknesses, columns=self.opportunities)
        self.st_letters = pd.DataFrame(index=strengths_letters, columns=threats_letters)
        self.so_letters = pd.DataFrame(index=strengths_letters, columns=opportunities_letters)
        self.wt_letters = pd.DataFrame(index=weaknesses_letters, columns=threats_letters)
        self.wo_letters = pd.DataFrame(index=weaknesses_letters, columns=opportunities_letters)

        st['High production price'] = [0.0, 0.09, 0.4, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.6, ]
        st['High service price'] = [0.4, 0.3, 0.4, 0.4, 0.1, 0.2, 0.8, 0.0, 0.1, 0.0, 0.0, 0.2, ]
        st['Not enough qualified mechanics'] = [0.0, 0.5, 0.4, 0.1, 0.8, 0.0, 0.65, 0.0, 0.33, 0.0, 0.0, 0.0, ]
        st['Bad road cover surface'] = [0.4, 0.7, 0.6, 0.45, 0.75, 0.0, 0.8, 0.5, 0.0, 0.1, 0.0, 0.3, ]
        st['Not ordinary behaivor of some road users'] = [0.8, 0.9, 0.6, 1.0, 0.05, 0.0, 0.3, 0.0, 0.0, 0.5, 0.0, 0.0, ]
        st['Rejection by people'] = [0.0, .95, 0.0, 0.8, 0.0, 0.25, .9, 0.17, 0.5, 0.8, 0.05, .84, ]
        st['Hacking, confidentiality problems'] = [.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.2, 0.0, 0.0, 0.0, ]
        st['Increased scam interest'] = [.75, 0.2, 0.0, 0.0, 0.0, 0.12, 0.1, 0.4, 0.3, 0.0, 0.0, 0.7, ]
        st['Job abolition'] = [0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.0, 0.0, 0.7, ]
        st['Inadequacy of legal system'] = [0.0, 0.4, 0.5, 0.2, 0.32, 0.0, 0.98, 0.0, 0.0, 0.28, 0.0, 0.0, ]

        self.st_letters['T1'] = [0.0, 0.09, 0.4, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.6, ]
        self.st_letters['T2'] = [0.4, 0.3, 0.4, 0.4, 0.1, 0.2, 0.8, 0.0, 0.1, 0.0, 0.0, 0.2, ]
        self.st_letters['T3'] = [0.0, 0.5, 0.4, 0.1, 0.8, 0.0, 0.65, 0.0, 0.33, 0.0, 0.0, 0.0, ]
        self.st_letters['T4'] = [0.4, 0.7, 0.6, 0.45, 0.75, 0.0, 0.8, 0.5, 0.0, 0.1, 0.0, 0.3, ]
        self.st_letters['T5'] = [0.8, 0.9, 0.6, 1.0, 0.05, 0.0, 0.3, 0.0, 0.0, 0.5, 0.0, 0.0, ]
        self.st_letters['T6'] = [0.0, .95, 0.0, 0.8, 0.0, 0.25, .9, 0.17, 0.5, 0.8, 0.05, .84, ]
        self.st_letters['T7'] = [.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.2, 0.0, 0.0, 0.0, ]
        self.st_letters['T8'] = [.75, 0.2, 0.0, 0.0, 0.0, 0.12, 0.1, 0.4, 0.3, 0.0, 0.0, 0.7, ]
        self.st_letters['T9'] = [0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3, 0.0, 0.0, 0.7, ]
        self.st_letters['T10'] = [0.0, 0.4, 0.5, 0.2, 0.32, 0.0, 0.98, 0.0, 0.0, 0.28, 0.0, 0.0, ]
        st.style.background_gradient(cmap='Oranges', axis=None)

        so["E-maps of road signs"] = [0.5, 0.4, 0.8, 0.9, 0.0, 0.2, 0.7, 0.9, 0.0, 0.3, 0.8, 0.0]
        so["Vehicle to vehicle connection"] = [0.0, 0.2, 0.4, 0.55, 0.0, 0.0, 0.25, 0.25, 0.2, 0.7, 0.0, 0.0]
        so["More passanger places (no driver needed)"] = [0.99, 0.8, 0.6, 0.8, 0.2, 0.8, 0.92, 0.9, 0.5, 0.93, 0.4, 0.8]
        so["System to prevent trafic jams"] = [0.86, 0.97, 0.9, 0.85, 0.15, 0.45, 0.85, 1.0, 0.2, 0.1, 0.0, 0.7]
        so["Alternative energy usage"] = [0.0, 0.0, 0.3, 0.2, 0.0, 0.0, 0.35, 0.28, 0.95, 0.2, 0.0, 0.1]
        so["New powerful computer vision technologies"] = [0.41, 0.0, 0.31, 0.7, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.75,
                                                           0.0]
        so["Cars technologies with less polution"] = [0.8, 0.0, 0.69, 0.54, 0.0, 0.2, 0.3, 0.75, 0.88, 0.0, 0.0, 0.62]
        so["High efficency engines"] = [0.8, 0.0, 0.5, 0.2, 0.3, 0.0, 0.21, 0.2, 0.8, 0.0, 0.0, 0.0]
        so["High demand on cars"] = [0.9, 0.85, 0.1, 0.6, 0.07, 0.36, 0.28, 0.65, 0.7, 0.0, 0.42, 0.9]
        so["Goverment support of autonomous cars dev"] = [0.65, 0.95, 0.8, 0.75, 0.0, 0.39, 1.0, 0.0, 0.5, 0.8, 0.0,
                                                          0.59]

        self.so_letters['O1'] = [0.5, 0.4, 0.8, 0.9, 0.0, 0.2, 0.7, 0.9, 0.0, 0.3, 0.8, 0.0]
        self.so_letters['O2'] = [0.0, 0.2, 0.4, 0.55, 0.0, 0.0, 0.25, 0.25, 0.2, 0.7, 0.0, 0.0]
        self.so_letters['O3'] = [0.99, 0.8, 0.6, 0.8, 0.2, 0.8, 0.92, 0.9, 0.5, 0.93, 0.4, 0.8]
        self.so_letters['O4'] = [0.86, 0.97, 0.9, 0.85, 0.15, 0.45, 0.85, 1.0, 0.2, 0.1, 0.0, 0.7]
        self.so_letters['O5'] = [0.0, 0.0, 0.3, 0.2, 0.0, 0.0, 0.35, 0.28, 0.95, 0.2, 0.0, 0.1]
        self.so_letters['O6'] = [0.41, 0.0, 0.31, 0.7, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.75, 0.0]
        self.so_letters['O7'] = [0.8, 0.0, 0.69, 0.54, 0.0, 0.2, 0.3, 0.75, 0.88, 0.0, 0.0, 0.62]
        self.so_letters['O8'] = [0.8, 0.0, 0.5, 0.2, 0.3, 0.0, 0.21, 0.2, 0.8, 0.0, 0.0, 0.0]
        self.so_letters['O9'] = [0.9, 0.85, 0.1, 0.6, 0.07, 0.36, 0.28, 0.65, 0.7, 0.0, 0.42, 0.9]
        self.so_letters['O10'] = [0.65, 0.95, 0.8, 0.75, 0.0, 0.39, 1.0, 0.0, 0.5, 0.8, 0.0, 0.59]
        so.style.background_gradient(cmap='Greens', axis=None)

        wt['High production price'] = [0.1, 0.85, 0.33, 0.4, 0.0, 0.5, 0.4, 0.0, 0.0, 0.6, 0.9, 0.0, ]
        wt['High service price'] = [0.7, 0.0, 0.4, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.35, 0.23, 0.1, ]
        wt['Not enough qualified mechanics'] = [0.65, 0.0, 0.25, 0.0, 0.1, 0.0, 0.3, 0.2, 0.0, 0.6, 0.44, 0.0, ]
        wt['Bad road cover surface'] = [0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.0, 0.15, 0.3, 0.1, ]
        wt['Not ordinary behaivor of some road users'] = [0.69, 0.9, 0.02, 0.95, 1.0, 0.0, 0.67, 0.8, 0.75, 0.6, 0.0,
                                                          0.8, ]
        wt['Rejection by people'] = [0.0, 0.0, 0.0, 0.6, 0.85, 0.45, 0.0, 0.1, 1.0, 0.34, 0.18, 0.59, ]
        wt['Hacking, confidentiality problems'] = [0.0, 0.0, 0.0, 0.0, 0.1, 0.99, 0.2, 0.0, 0.35, 0.5, 0.0, 0.2, ]
        wt['Increased scam interest'] = [0.0, 0.0, 0.0, 0.1, 0.4, 0.75, 0.35, 0.0, 0.4, 0.65, 0.95, 0.15, ]
        wt['Job abolition'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.1, 0.1, ]
        wt['Inadequacy of legal system'] = [0.0, 0.0, 0.0, 0.7, 0.92, 0.65, 0.0, 0.25, 1.0, 0.35, 0.25, 0.4, ]

        self.wt_letters['T1'] = [0.1, 0.85, 0.33, 0.4, 0.0, 0.5, 0.4, 0.0, 0.0, 0.6, 0.9, 0.0, ]
        self.wt_letters['T2'] = [0.7, 0.0, 0.4, 0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.35, 0.23, 0.1, ]
        self.wt_letters['T3'] = [0.65, 0.0, 0.25, 0.0, 0.1, 0.0, 0.3, 0.2, 0.0, 0.6, 0.44, 0.0, ]
        self.wt_letters['T4'] = [0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.0, 0.15, 0.3, 0.1, ]
        self.wt_letters['T5'] = [0.69, 0.9, 0.02, 0.95, 1.0, 0.0, 0.67, 0.8, 0.75, 0.6, 0.0, 0.8, ]
        self.wt_letters['T6'] = [0.0, 0.0, 0.0, 0.6, 0.85, 0.45, 0.0, 0.1, 1.0, 0.34, 0.18, 0.59, ]
        self.wt_letters['T7'] = [0.0, 0.0, 0.0, 0.0, 0.1, 0.99, 0.2, 0.0, 0.35, 0.5, 0.0, 0.2, ]
        self.wt_letters['T8'] = [0.0, 0.0, 0.0, 0.1, 0.4, 0.75, 0.35, 0.0, 0.4, 0.65, 0.95, 0.15, ]
        self.wt_letters['T9'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.1, 0.1, ]
        self.wt_letters['T10'] = [0.0, 0.0, 0.0, 0.7, 0.92, 0.65, 0.0, 0.25, 1.0, 0.35, 0.25, 0.4, ]
        wt.style.background_gradient(cmap='Reds', axis=None)

        wo["E-maps of road signs"] = [0.0, 0.9, 0.2, 0.0, 0.05, 0.3, 0.8, 0.1, 0.0, 0.48, 0.75, 0.0]
        wo["Vehicle to vehicle connection"] = [0.1, 0.96, 0.3, 0.0, 0.0, 0.7, 1.0, 0.83, 0.22, 0.56, 0.8, 0.0]
        wo["More passanger places (no driver needed)"] = [0.3, 0.7, 0.0, 0.0, 0.8, 0.0, 0.9, 0.0, 0.76, 0.7, 0.5, 0.1]
        wo["System to prevent trafic jams"] = [0.2, 0.8, 0.08, 0.6, 0.3, 0.2, 0.7, 0.6, 0.4, 0.4, 0.83, 0.0]
        wo["Alternative energy usage"] = [0.7, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13, 0.35, 0.0]
        wo["New powerful computer vision technologies"] = [0.22, 0.9, 0.65, 0.4, 0.35, 0.12, 0.0, 0.08, 0.0, 0.5, 0.4,
                                                           0.0]
        wo["Cars technologies with less polution"] = [0.5, 0.0, 0.37, 0.0, 0.0, 0.0, 0.3, 0.0, 0.2, 0.21, 0.12, 0.0]
        wo["High efficency engines"] = [0.43, 0.0, 0.25, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.1, 0.0, 0.0]
        wo["High demand on cars"] = [0.3, 0.0, 0.5, 0.6, 0.25, 0.4, 0.15, 0.1, 0.39, 0.7, 0.9, 0.0]
        wo["Goverment support of autonomous cars dev"] = [0.0, 0.37, 0.3, 0.3, 0.9, 0.6, 0.1, 0.09, 0.99, 0.65, 0.0,
                                                          0.39]

        self.wo_letters['O1'] = [0.0, 0.9, 0.2, 0.0, 0.05, 0.3, 0.8, 0.1, 0.0, 0.48, 0.75, 0.0]
        self.wo_letters['O2'] = [0.1, 0.96, 0.3, 0.0, 0.0, 0.7, 1.0, 0.83, 0.22, 0.56, 0.8, 0.0]
        self.wo_letters['O3'] = [0.3, 0.7, 0.0, 0.0, 0.8, 0.0, 0.9, 0.0, 0.76, 0.7, 0.5, 0.1]
        self.wo_letters['O4'] = [0.2, 0.8, 0.08, 0.6, 0.3, 0.2, 0.7, 0.6, 0.4, 0.4, 0.83, 0.0]
        self.wo_letters['O5'] = [0.7, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.13, 0.35, 0.0]
        self.wo_letters['O6'] = [0.22, 0.9, 0.65, 0.4, 0.35, 0.12, 0.0, 0.08, 0.0, 0.5, 0.4, 0.0]
        self.wo_letters['O7'] = [0.5, 0.0, 0.37, 0.0, 0.0, 0.0, 0.3, 0.0, 0.2, 0.21, 0.12, 0.0]
        self.wo_letters['O8'] = [0.43, 0.0, 0.25, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.1, 0.0, 0.0]
        self.wo_letters['O9'] = [0.3, 0.0, 0.5, 0.6, 0.25, 0.4, 0.15, 0.1, 0.39, 0.7, 0.9, 0.0]
        self.wo_letters['O10'] = [0.0, 0.37, 0.3, 0.3, 0.9, 0.6, 0.1, 0.09, 0.99, 0.65, 0.0, 0.39]

        wo.style.background_gradient(cmap='Blues', axis=None)

        swot = pd.concat([pd.concat([st, so], axis=1), pd.concat([wt, wo], axis=1)], axis=0)
        swot_letteres = pd.concat((pd.concat((self.st_letters, self.so_letters), axis=1), pd.concat((self.wt_letters,
                                                                                                     self.wo_letters),
                                                                                                    axis=1)), axis=0)

        return swot, swot_letteres
