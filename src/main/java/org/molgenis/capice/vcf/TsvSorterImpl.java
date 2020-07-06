package org.molgenis.capice.vcf;

import static org.molgenis.capice.vcf.TsvUtils.TSV_FORMAT;

import com.google.code.externalsorting.csv.CsvExternalSort;
import com.google.code.externalsorting.csv.CsvSortOptions;
import java.io.File;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.List;
import org.springframework.stereotype.Component;

@Component
public class TsvSorterImpl implements TsvSorter {

  @Override
  public void sortTsv(Path inputTsv, Path outputTsv, File tempDir) {
    CsvSortOptions sortOptions =
        new CsvSortOptions.Builder(
                CsvExternalSort.DEFAULTMAXTEMPFILES,
                new TsvRecordComparator(),
                1,
                CsvExternalSort.estimateAvailableMemory())
            .charset(StandardCharsets.UTF_8)
            .distinct(false)
            .numHeader(1)
            .skipHeader(false)
            .format(TSV_FORMAT)
            .build();

    try {
      List<File> sortInBatch =
          CsvExternalSort.sortInBatch(
              inputTsv.toFile(), tempDir, sortOptions);
      CsvExternalSort.mergeSortedFiles(sortInBatch, outputTsv.toFile(), sortOptions, true);
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    } catch (ClassNotFoundException e) {
      throw new IllegalStateException(e);
    }
  }
}
