#!/usr/bin/env python3

"""
A parser of SMILES chemical notation using pyparsing module the EBNF of SMILES
is taken from:
https://metamolecular.com/cheminformatics/smiles/railroad-diagram/
"""

import pyparsing as pp

# Grammar definition
isotope = pp.Regex('[1-9][0-9]?[0-9]?')
atomclass = pp.Regex(':[0-9]+')
bond = pp.oneOf(['-','=','#','$',':','/','\\','.'])
organicsymbol = pp.oneOf(['B','Br','C','Cl','N','O','P','S','F','I'])
aromaticsymbol = pp.oneOf(['b','c','n','o','p','s'])
elementsymbol = pp.oneOf(['Al','Am','Sb','Ar','33','At','Ba','Bk','Be','Bi',
                           'Bh','B','Br','Cd','Ca','Cf','C','Ce','Cs','Cl','Cr',
                           'Co','Cu','Cm','Ds','Db','Dy','Es','Er','Eu','Fm',
                           'F','Fr','Gd','Ga','Ge','Au','Hf','Hs','He','Ho','H',
                           'In','I','Ir','Fe','Kr','La','Lr','Pb','Li','Lu','Mg',
                           'Mn','Mt','Md','Hg','Mo','Nd','Ne','Np','Ni','Nb','N',
                           'No','Os','O','Pd','P','Pt','Pu','Po','K','Pr','Pm',
                           'Pa','Ra','Rn','Re','Rh','Rg','Rb','Ru','Rf','Sm',
                           'Sc','Sg','Se','Si','Ag','Na','Sr','S','Ta','Tc',
                           'Te','Tb','Tl','Th','Tm','Sn','Ti','W','Uub','Uuh',
                           'Uuo','Uup','Uuq','Uus','Uut','Uuu','U','V','Xe','Yb',
                           'Y','Zn','Zr',])
hcount = pp.Regex('H[0-9]+')
ringclosure = pp.Optional( pp.Literal('%') + pp.oneOf(['1 2 3 4 5 6 7 8 9'])) + pp.oneOf(['0 1 2 3 4 5 6 7 8 9'])
charge = (pp.Literal('-') +  pp.Optional( pp.oneOf(['-02-9']) ^ pp.Literal('1') + pp.Optional(pp.oneOf(['0-5'])) )) ^ pp.Literal('+') + pp.Optional( pp.oneOf(['+02-9']) ^ pp.Literal('1') + pp.Optional(pp.oneOf('[0-5]')) )
chiralclass = pp.Optional(pp.Literal('@') + pp.Optional( pp.Literal('@')) ^ ( pp.Literal('TH') ^ pp.Literal('AL') ) + pp.oneOf('[1-2]') ^ pp.Literal('SP') + pp.oneOf('[1-3]') ^ pp.Literal('TB') + ( pp.Literal('1') + pp.Optional(pp.oneOf('[0-9]')) ^ pp.Literal('2') + pp.Optional(pp.Literal('0')) ^ pp.oneOf('[3-9]') ) ^ pp.Literal('OH') + ( ( pp.Literal('1') ^ pp.Literal('2') ) + pp.Optional(pp.oneOf('[0-9]')) ^ pp.Literal('3') + pp.Optional(pp.Literal('0')) ^ pp.oneOf('[4-9]')) )
atomspec = pp.Literal('[') +  pp.Optional(isotope) + ( pp.Literal('se') ^ pp.Literal('as') ^ aromaticsymbol ^ elementsymbol ^ pp.Literal('*') ) + pp.Optional(chiralclass)+ pp.Optional(hcount)+pp.Optional(charge)+ pp.Optional(atomclass) + pp.Literal(']')
atom = organicsymbol ^ aromaticsymbol ^ pp.Literal('*') ^ atomspec
chain = pp.OneOrMore(pp.Optional(bond) + ( atom ^ ringclosure ))
## This looks fucked up
smiles = pp.Forward()
branch = pp.Forward()
smiles << atom + pp.ZeroOrMore(chain ^ branch)
branch << (pp.Literal('(') + (bond ^ pp.OneOrMore(smiles)) + pp.Literal(')'))



def IsValidSMILES(text):
    """
    A simple SMILES validator
    """
    is_valid = False
    results = smiles.parseString(text)
    if results:
        is_valid = True
        return(is_valid)
    return is_valid

if __name__ == '__main__':
    astr = 'CC(CC)CO[Na+]'
    print(IsValidSMILES(astr)) 
