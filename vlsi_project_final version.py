import itertools  # Βιβλιοθήκη για επαναλήψεις

# TECHNOLOGY LIBRARY
TECH_LIB = {
    'INV':    {'area': 5,  'delay': 30, 'inputs': 1},
    'NAND2a': {'area': 8,  'delay': 40, 'inputs': 2},
    'NAND2b': {'area': 5,  'delay': 60, 'inputs': 2},
    'NOR2a':  {'area': 8,  'delay': 45, 'inputs': 2},
    'NOR2b':  {'area': 10, 'delay': 30, 'inputs': 2},
    'AND2a':  {'area': 10, 'delay': 50, 'inputs': 2},
    'AND2b':  {'area': 12, 'delay': 45, 'inputs': 2},
    'AND2c':  {'area': 16, 'delay': 40, 'inputs': 2},
    'OR2a':   {'area': 10, 'delay': 55, 'inputs': 2},
    'OR2b':   {'area': 20, 'delay': 35, 'inputs': 2},
    'XOR2':   {'area': 15, 'delay': 70, 'inputs': 2},
    'AND3':   {'area': 13, 'delay': 60, 'inputs': 3},
    'OR3':    {'area': 13, 'delay': 65, 'inputs': 3},
    'NAND3a': {'area': 11, 'delay': 50, 'inputs': 3},
    'NAND3b': {'area': 10, 'delay': 55, 'inputs': 3},
    'NOR3a':  {'area': 11, 'delay': 55, 'inputs': 3},
    'NOR3b':  {'area': 15, 'delay': 45, 'inputs': 3},
    'AND4a':  {'area': 16, 'delay': 70, 'inputs': 4},
    'AND4b':  {'area': 20, 'delay': 50, 'inputs': 4},
    'AND4c':  {'area': 26, 'delay': 45, 'inputs': 4},
    'OR4a':   {'area': 26, 'delay': 75, 'inputs': 4},
    'OR4b':   {'area': 28, 'delay': 65, 'inputs': 4},
    'OR4c':   {'area': 24, 'delay': 70, 'inputs': 4},
}

# 2. QUINE–McCLUSKEY (Αλγόριθμος Ελαχιστοποίησης)
class QM_Solver:
    def __init__(self, variables):
        self.variables = variables      # Λίστα με τα ονόματα μεταβλητών ['A', 'B', ...]
        self.n = len(variables)         # Το πλήθος τους

    def solve(self, minterms, dont_cares=[]):
        # Ενώνουμε minterms και don't cares για την ομαδοποίηση.Το set διαγράφει τα διπλότυπα.
        # Τα don't cares βοηθούν στην απλοποίηση αλλά δεν είναι υποχρεωτικό να καλυφθούν
        all_terms = set(minterms) | set(dont_cares)
        
        groups = {}
        for m in all_terms:
            b = format(m, f'0{self.n}b') # Μετατρέπει έναν αριθμό σε string. Εδώ πρόκειτε για εντολή μορφοποίησης. 
            # Δηλαδή φτιάχνετε ένας αριθμός και αν είναι μιρκός στο δυαδικό τον γεμίζουμε με μηδενικά στην αρχή
            groups.setdefault(b.count('1'), set()).add(b) # Εδώ βάζουμε σε ομάδες τους αριθμούς ανάλογα με το πόσα 1 έχουν.
            # Μετράμε πόσους άσσους έχει το string. Εδώ στην ουσία δημιουργείτε ένα λεξικό που συγκρατεί set με ομαδοποιήσεις ασσών

        primes = set() # Εδώ θα μαζέψουμε τους Prime Implicants
        while groups:
            new_groups = {} # Εδώ θα βάλουμε τα αποτελέσματα του επόμενου γύρου
            used = set() # Εδώ σημειώνουμε ποιους όρους καταφέραμε να ζευγαρώσουμε
            keys = sorted(groups) # Ταξινομούμε τα κλειδιά
            for i in range(len(keys)-1):  # Συγκρίνουμε κάθε ομάδα (i) με την αμέσως επόμενη (i+1)
                for a in groups[keys[i]]:
                    for b in groups[keys[i+1]]:
                        diff = [j for j in range(self.n) if a[j] != b[j]] # Εδώ συγκρίνουμε δύο strings και ψάχνουμε σε ποιες θέσεις διαφέρουν.
                        if len(diff) == 1: # Μπορούμε να ενώσουμε δύο όρους μόνο αν διαφέρουν σε ακριβώς ένα bit.
                            j = diff[0]
                            merged = a[:j] + '-' + a[j+1:] # Φτιάχνουμε τον καινούργιο όρο που έχει παύλα εκεί που διέφερουν.
                            new_groups.setdefault(merged.count('1'), set()).add(merged)
                            used |= {a, b} # Εδώ κρατάμε στην λίστα αυτούς που δεν είναι prime implicants
            for g in groups.values(): # Όσοι όροι υπήρχαν στις ομάδες αλλά δεν μπήκαν στα 'used', σημαίνει ότι δεν ταίριαξαν με κανέναν. Άρα Prime Implicants
                for t in g:
                    if t not in used:
                        # Κρατάμε έναν όρο μόνο αν δεν είναι καθαρό don't care. Εδώ το κρατάμε απλά ως Prime Implicant.
                        primes.add(t)
            groups = new_groups
            selected_primes = list(primes)
            
        # Φιλτράρισμα: Θέλουμε να καλύψουμε τα minterms, τα don't cares δεν μας νοιάζουν στο τέλος
        return list(primes), selected_primes

    def to_sop(self, pis): # Εδώ με μετατρέπουμε τους όρους σε μορφή κειμένου
        terms = []
        for pi in pis:
            parts = []
            for i, c in enumerate(pi): # Θα ελέγξουμε κάθε γράμμα και τη θέση του
                if c == '1':
                    parts.append(self.variables[i])      # Αν είναι με 1 βάλε το γράμμα
                elif c == '0':
                    parts.append(self.variables[i] + "'") # Αν είναι με 0 βάλε το γράμμα με τόνο
                # Αν είναι '-', απλοποιήθηκε
            terms.append("*".join(parts)) # Ενώνουμε με AND (*)
        return " + ".join(terms)          # Ενώνουμε τους όρους με OR (+)

# 3. TECHNOLOGY MAPPING (Χαρτογράφηση σε Πύλες)
class TechMapper:
    def __init__(self, lib):
        self.lib = lib # Αποθηκεύουμε τη βιβλιοθήκη

    def best_gate(self, prefix, inputs):
        # Ψάχνουμε στη βιβλιοθήκη για πύλες που ξεκινούν με το prefix και έχουν τον σωστό αριθμό εισόδων. Επιστρέφουμε αυτή με το μικρότερο εμβαδόν.
        cands = [(n, g) for n, g in self.lib.items() # Φτιάχνουμε μια λίστα που έχει ζευγάρια για τις πύλες που το όνομα και ο αριθμός εισόδων είναι αυτό που ζητήσαμε.
                 if n.startswith(prefix) and g['inputs'] == inputs]
        # Επιστρέφει αυτή με το μικρότερο 'area'
        return min(cands, key=lambda x: x[1]['area'])

    def map_sop(self, sop): # Μετατρέπει το SOP string σε Netlist
        if sop == "0" or sop == "1": return [], 0, 0  # Αν το SOP είναι κενό ή 0/1
        terms = sop.split(" + ") # Χωρίζουμε τα OR (τα +)
        netlist = []    # Εδώ θα αποθηκεύσουμε τις πύλες μας
        invs = set()    # Ένα set για να θυμόμαστε ποιες μεταβλητές έχουμε ήδη αντιστρέψει (για να μην βάζουμε διπλούς inverters)
        and_outs = []   # Λίστα για να μαζέψουμε τα καλώδια που βγαίνουν από τις πύλες AND
        area = 0        # Συνολικό εμβαδόν
        delays = []     # Υπολογίζουμε τις καθυστερήσεις
        
        for t in terms: # Δημιουργία AND πυλών
            lits = t.split("*") # Βρίσουμε τις μεταβλητές
            ins = []            # Φτιάχνουμε προσωρινή λίστα για τις εισόδους της τρέχουσας πύλης AND
            inv_delay = 0       # Μεταβλητή για να κρατήσουμε την καθυστέρηση αν υπάρχει inverter

            for l in lits: # Για κάθε γράμμα στον όρο
                if "'" in l: # Αν έχει τόνο
                    v = l.replace("'", "") # Αφαίρεσε τον τόνο για να βρεις το όνομα.
                    
                    # Αν δεν έχουμε φτιάξει ήδη inverter για αυτό το σήμα
                    if v not in invs: # Αν όχι, βρες τον καλύτερο INV από τη βιβλιοθήκη
                        g, spec = self.best_gate("INV", 1)
                        netlist.append((g, [v], v+"_n")) # Προσθήκη στο netlist
                        area += spec['area'] # Πρόσθεσε το εμβαδόν του
                        invs.add(v) # Το v έχει αντιστραφεί
                        
                    ins.append(v+"_n") # Η είσοδος της AND είναι η έξοδος του Inverter
                    inv_delay = spec['delay'] # Κρατάμε την καθυστέρηση
                else:
                    ins.append(l) # Αν δεν έχει τόνο, απλά βάλε το όνομα στη λίστα εισόδων

            if len(ins) > 1:   # Αν έχουμε > 1 εισόδους, θέλουμε πύλη AND
                g, spec = self.best_gate("AND", len(ins))
                out = f"and_{len(and_outs)}" # Φτιάχνουμε ένα μοναδικό όνομα για το καλώδιο εξόδου
                netlist.append((g, ins, out)) # Προσθέτουμε την πύλη στο Netlist
                area += spec['area']
                
                delays.append(inv_delay + spec['delay']) # Υπολογισμός καθυστέρησης αυτού του κλαδιού.
                and_outs.append(out) # Κρατάμε το όνομα εξόδου για να το βάλουμε μετά στην OR
            else:
                # Αν είναι μόνο μία μεταβλητή, δεν θέλει πύλη AND και το καλώδιο πάει απευθείας στην επόμενη φάση.
                and_outs.append(ins[0])

        if len(and_outs) > 1: #Δημιουργία OR πύλης
            g, spec = self.best_gate("OR", len(and_outs)) # Αν έχουμε πολλά σήματα από τις AND, τα βάζουμε σε μια OR
            netlist.append((g, and_outs, "F")) # Η έξοδος αυτής της πύλης είναι η τελική έξοδος F
            area += spec['area']
            
            delays = [d + spec['delay'] for d in delays] # Προσθέτουμε την καθυστέρηση της OR σε όλα τα μονοπάτια που βρήκαμε πριν
        else:
            # Αν υπάρχει μόνο ένας όρος, κάνουμε απλά συνδέουμε την έξοδο της AND στην έξοδο F
            netlist.append(("ASSIGN", [and_outs[0]], "F"))

        return netlist, area, max(delays) if delays else 0 # Επιστρέφουμε τη λίστα, το συνολικό εμβαδόν και τη μέγιστη καθυστέρηση

    def to_verilog(self, netlist): # Εδώ μετατρέπουμε σε κώδικα verilog
        v = ["module logic_circuit(input A,B,C,D, output F);"] # Γράφουμε την επικεφαλίδα του module
        
        # Βρίσκουμε όλα τα εσωτερικά καλώδια (όχι την έξοδο F)
        wires = {o for _,_,o in netlist if o not in ("F")}
        if wires:
            v.append("  wire " + ", ".join(wires) + ";") # Δήλωση wires
            
        # Δημιουργία εντολών για κάθε πύλη
        for i,(g,ins,out) in enumerate(netlist):
            if g == "ASSIGN": # Αν είναι ανάθεση
                v.append(f"  assign {out} = {ins[0]};")
            else:   # Αν είναι πύλη
                v.append(f"  {g} U{i} ( {out}, {', '.join(ins)} );")
                
        v.append("endmodule")
        return "\n".join(v) # Ενώνουμε όλες τις γραμμές

# 4. Κυρίως πρόγραμμα
if __name__ == "__main__":

    variables = ['A','B','C','D'] # Ορίζουμε τα ονόματα των μεταβλητών μας
    minterms = [1,9,11,15]    # # Ορίζουμε τα minterms
    dont_cares = []

    # 1. Αρχική Λογική Έκφραση
    print("\n Αρχική Λογική Έκφραση:")
    print(f"    Minterms: {minterms}")
    print(f"    Don't Cares: {dont_cares}")
    print(f"    Variables: {variables}")
    
    # 2. Λίστα Prime & Essential Implicants
    qm = QM_Solver(variables)
    all_pis, selected_pis = qm.solve(minterms, dont_cares)

    print("\n Λίστα Prime Implicants:")
    print(f"    All Prime Implicants (Binary): {all_pis}")
    # Σημείωση: Στην εργασία, τα Selected είναι αυτά που απαρτίζουν το Essential cover
    print(f"    Selected/Essential Implicants: {selected_pis}")
    
    # 3. Ελαχιστοποιημένη SOP
    sop = qm.to_sop(selected_pis)
    print("\n Ελαχιστοποιημένη Έκφραση (SOP):")
    print(f"    F = {sop}")

    mapper = TechMapper(TECH_LIB) # Δημιουργούμε ένα αντικείμενο της κλάσης TechMapper με τη βιβλιοθήκη TECH_LIB
    netlist, area, delay = mapper.map_sop(sop) # Του δίνουμε το SOP και του ζητάμε να το χτίσει με πύλες και μας επιστρέφει netlist, areα, delay.

    print("\nTechnology Mapping:")
    print(" Total Area:", area)
    print(" Critical Path Delay:", delay, "ps")

    print("\nVerilog:\n")
    print(mapper.to_verilog(netlist)) # Ζητάμε από τον mapper να μεταφράσει το netlist σε κώδικα Verilog