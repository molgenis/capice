package org.molgenis.capice.vcf;

import static org.molgenis.capice.vcf.TsvUtils.TSV_FORMAT;

import com.google.code.externalsorting.csv.CsvExternalSort;
import com.google.code.externalsorting.csv.CsvSortOptions;
import java.io.File;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;
import org.springframework.stereotype.Component;

@Component
public class TsvSorterImpl implements TsvSorter {

  @Override
  public void sortTsv(Path inputTsv, Path outputTsv) {
    try {
      writeTsvHeader(inputTsv, outputTsv);
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }

    try {
      // workaround for https://github.com/lemire/externalsortinginjava/issues/31
      CsvSortOptions sortInBatchOptions = createCsvSortOptionsBuilder().numHeader(1).build();
      List<File> sortInBatch = CsvExternalSort.sortInBatch(inputTsv.toFile(), null, sortInBatchOptions);

      CsvSortOptions mergeSortedFilesOptions = createCsvSortOptionsBuilder().build();
      CsvExternalSort.mergeSortedFiles(sortInBatch, outputTsv.toFile(), mergeSortedFilesOptions, true);
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    } catch (ClassNotFoundException e) {
      throw new IllegalStateException(e);
    }
  }

  private void writeTsvHeader(Path inputTsv, Path outputTsv) throws IOException {
    String headerLine;
    try (Stream<String> lineStream = Files.lines(inputTsv, StandardCharsets.UTF_8)) {
      headerLine = lineStream.findFirst().orElseThrow();
    }
    headerLine += TSV_FORMAT.getRecordSeparator();
    Files.writeString(outputTsv, headerLine, StandardCharsets.UTF_8);
  }

  private CsvSortOptions.Builder createCsvSortOptionsBuilder() {
    return new CsvSortOptions.Builder(
        CsvExternalSort.DEFAULTMAXTEMPFILES,
        new TsvRecordComparator(),
        1,
        CsvExternalSort.estimateAvailableMemory())
        .charset(StandardCharsets.UTF_8)
        .distinct(false)
        .format(TSV_FORMAT);
  }
}
