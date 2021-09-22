import pysam
from src.main.python.core.global_manager import CapiceManager
import logging
logger = logging.getLogger(__name__)


class FastaLookupAnnotator:
    def __init__(self):
        self.manager = CapiceManager()
        self.fasta_loc = self.manager.reference_genome
        self.fasta = None
        # self._load_fasta()

    def _load_fasta(self):
        logger.info('Loading in Fasta file, this may take a moment.')
        self.fasta = pysam.FastaFile(self.fasta_loc)
        logger.info(f'Succesfully loaded Fasta file at: {self.fasta_loc}')

    def get_reference_sequence(self, chromosome: str, start: int, end: int):
        """
        Function to obtain a sequence from the reference Fasta file.

        :param chromosome: string,
            chromosome to get the reference sequence from.
        :param start: Chromosomal position at what point the sequence
        should be obtained.

        :param end: Chromosomal position at what point the obtained sequence
        should end.

        :return: string, obtained reference sequence.
        """
        try:
            logger.debug(
                'Obtaining reference sequence for: '
                f'[Chromosome: {chromosome}], [start: {start}], [stop: {end}]'
            )
            append_ns = False
            if start < 0:
                append_ns = abs(start)
                start = 0
            return_sequence = self.fasta.fetch(chromosome, start, end)
            if append_ns:
                return_sequence = '{}{}'.format(
                    'N' * append_ns, return_sequence
                )
            return return_sequence
        except KeyError:
            logger.warning(
                'Unable to obtain sequence for: '
                '[Chromosome: {}], [start: {}], [stop: {}],'
                'did you supply a reference with contigs 1-22 + x,y,mt?',chromosome, start, end
            )
            return None

    def close_connection(self):
        """
        Function to tell pysam to close the connection to the Fasta file
        """
        if self.fasta:
            self.fasta.close()
