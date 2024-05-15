TOTAL_SIMULATION_TIME = 200  # [s]


class Measurement:
    CASE_TAG = "Case"
    ITV_TAG = "Generation Interval"
    GEN_TAG = "Packets Generated"
    DELIVERED_TAG = "Packets Delivered"
    DROPQ_TAG = "Dropped on Queue"
    DROPR_TAG = "Dropped on Receiver"
    TOTALDROP_TAG = "Dropped Packets"
    AVDEL_TAG = "Average Delay"
    GENRATE_TAG = "Generation Rate"
    RECRATE_TAG = "Reception Rate"


    def __init__(self, case, itv, gen, delivered, dropQ, dropR, avdel):
        self.case = case
        self.itv = float(itv)
        self.gen = int(gen)
        self.delivered = int(delivered)
        self.dropQ = int(dropQ)
        self.dropR = int(dropR)
        self.total_drop = self.dropQ + self.dropR
        self.avdel = float(avdel)
        self.gen_per_second = self.gen / TOTAL_SIMULATION_TIME
        self.rec_per_second = self.delivered / TOTAL_SIMULATION_TIME


    def __str__(self) -> str:
        return str(self.to_dictionary())

    def to_dictionary(self) -> dict:
        return {
            self.CASE_TAG: self.case,
            self.ITV_TAG: self.itv,
            self.GEN_TAG: self.gen,
            self.DELIVERED_TAG: self.delivered,
            self.DROPQ_TAG: self.dropQ,
            self.DROPR_TAG: self.dropR,
            self.TOTALDROP_TAG: self.total_drop,
            self.AVDEL_TAG: self.avdel,
            self.GENRATE_TAG: self.gen_per_second,
            self.RECRATE_TAG: self.rec_per_second,
        }

    @staticmethod
    def parse(line: str, case: str):
        """
        Parses a line like `| 2.0 | 144 | 144 | 0 | 0 | 0.40 |`
        to a Measurement instance
        """
        line = "".join(list(filter(lambda ch: ch != " ", line))).strip()
        args = line.split("|")[1:-1]
        args.insert(0, case)
        return Measurement(*args)