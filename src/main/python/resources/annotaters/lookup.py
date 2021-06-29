import pandas as pd
import pysam
import numpy as np
from src.main.python.core.global_manager import CapiceManager
from src.main.python.core.logger import Logger
import time


class FastaLookupAnnotator:
    def __init__(self):
        self.log = Logger().logger
        self.manager = CapiceManager()
        self.fasta_loc = self.manager.reference_genome
        self.fasta = None
        self._load_fasta()

    def _load_fasta(self):
        self.log.info('Loading in Fasta file, this may take a moment.')
        self.fasta = pysam.FastaFile(self.fasta_loc)
        self.log.info('Succesfully loaded Fasta file at: {}'.format(self.fasta_loc))

    def get_reference_sequence(self, chromosome: str, start: int, end: int):
        """
        Function to obtain a sequence from the reference Fasta file.

        :param chromosome: string, chromosome to get the reference sequence from.
        :param start: Chromosomal position at what point the sequence should be obtained.
        :param end: Chromosomal position at what point the obtained sequence should end.
        :return: string, obtained reference sequence.
        """
        try:
            self.log.debug(
                'Obtaining reference sequence for: [Chromosome: {}], [start: {}], [stop: {}]'.format(chromosome, start,
                                                                                                     end))
            append_ns = False
            if start < 0:
                append_ns = abs(start)
                start = 0
            return_sequence = self.fasta.fetch(chromosome, start, end)
            if append_ns:
                return_sequence = '{}{}'.format('N' * append_ns, return_sequence)
            return return_sequence
        except KeyError:
            self.log.warning(
                'Unable to obtain sequence for: [Chromosome: {}], [start: {}], [stop: {}],'
                'did you supply a reference with contigs 1-22 + x,y,mt?'.format(chromosome, start, end))
            return None

    def close_connection(self):
        """
        Function to tell pysam to close the connection to the Fasta file
        """
        if self.fasta:
            self.fasta.close()


class LookupAnnotator:
    """
    First split them into SNVs and InDels.
    Lookup SNVs first
    Then lookup InDels
    If indel not in InDels_inclAnno.tsv.gz: put out warning and use impute values instead
    """
    def __init__(self):
        self.log = Logger().logger
        self.manager = CapiceManager()
        self.dataset = pd.DataFrame
        self.header = []
        self.snvs_database = self.manager.cadd_snvs_database
        self.indels_database = self.manager.cadd_indels_database
        self.snvs = None
        self.indels = None
        self._load_snvs_database()
        self._load_indels_database()
        self.lookup_cols = []
        self.total = 0
        self.n_now = 0
        self.now = 0

    def _load_snvs_database(self):
        self.log.info('Loading in CADD SNVs database, please hold.')
        self.snvs = pysam.TabixFile(self.snvs_database)
        self.log.info('Succesfully loaded CADD SNVs database at: {}'.format(self.snvs_database))

    def _load_indels_database(self):
        self.log.info('Loading in CADD InDels database, please hold.')
        self.indels = pysam.TabixFile(self.indels_database)
        self.log.info('Succesfully loaded CADD InDels database at: {}'.format(self.indels_database))

    def close_connections(self):
        """
        Function to close the file connection to the CADD SNVs database and CADD InDels database.
        """
        self.snvs.close()
        self.indels.close()

    def _get_to_lookup_columns(self):
        self.header = self.snvs.header[1].split('#')[1].split('\t')
        for column in self.header:
            if column not in self.dataset:
                self.lookup_cols.append(column)

    def process(self, dataset: pd.DataFrame):
        """
        Function to get the Lookup annotations for the manually annotated dataframe.
        :param dataset: Pandas.DataFrame
        :return: Pandas.DataFrame
        """
        self.dataset = dataset
        self._get_to_lookup_columns()
        self.total = self.dataset.shape[0]
        self.now = time.time()
        self.dataset.apply(lambda x: self._get_lookup_annotations(x), axis=1)
        return self.dataset

    def _timer(self):
        time_iwl = time.time()
        if time_iwl - self.now > 30:
            self.log.info('Still processing, currently done: {}/{} ({}%)'.format(self.n_now, self.total,
                                                                                 round(self.n_now/self.total*100)))
            self.now = time.time()

    def _get_lookup_annotations(self, row: pd.Series):
        chromosome = row['Chr']
        pos = row['Pos']
        ref = row['Ref']
        alt = row['Alt']
        consdetail = row['ConsDetail']
        if row['Type'] == 'SNV':
            retrieved = self._get_snvs_annotations(chromosome, pos)
        else:
            retrieved = self._get_indels_annotations(chromosome, pos)
        res = self._post_process_retrieve(retrieved, chromosome, pos, ref, alt, consdetail)
        self.dataset.loc[row.name, self.lookup_cols] = res
        self._timer()
        self.n_now += 1

    def _post_process_retrieve(self, retrieved_list, chromosome, pos, ref, alt, consdetail):
        retrieval_dataframe = pd.DataFrame(retrieved_list, columns=self.header)
        retrieval_dataframe.replace(to_replace='NA', value=np.nan, inplace=True)
        retrieval_dataframe = retrieval_dataframe[
            (retrieval_dataframe['Ref'] == ref) &
            (retrieval_dataframe['Alt'] == alt) &
            (retrieval_dataframe['ConsDetail'] == consdetail)
            ]
        if retrieval_dataframe.shape[0] < 1:
            self.log.debug(
                'Could not retrieve data for chromosome: {}, pos: {}, ref: {}, alt: {} and consequence: {} ! '
                'Using impute values only!'.format(chromosome, pos, ref, alt, consdetail))
            return [None] * len(self.lookup_cols)
        else:
            return retrieval_dataframe[self.lookup_cols].values.tolist()[0]

    def _get_snvs_annotations(self, chromosome, pos):
        retrieval_list = []
        for line in self.snvs.fetch(chromosome, pos - 1, pos):
            retrieval_list.append(line.split('\t'))
        return retrieval_list

    def _get_indels_annotations(self, chromosome, pos):
        retrieval_list = []
        for line in self.indels.fetch(chromosome, pos-1, pos):
            retrieval_list.append(line.split('\t'))
        return retrieval_list
