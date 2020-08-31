package org.molgenis.capice.vcf;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class TsvSorterImplTest {

  @TempDir static Path sharedTempDir;

  @Test
  void sortTsv() throws IOException {

    Path inputPath = Paths.get("src", "test", "resources", "input_predictions.tsv");
    Path outputPath = sharedTempDir.resolve("output.tsv");

    TsvSorter tsvSorter = new TsvSorterImpl();

    tsvSorter.sortTsv(inputPath, outputPath);

    String actual =
        Files.readString(outputPath, StandardCharsets.UTF_8)
            .replaceAll("\\n|\\r\\n", System.getProperty("line.separator"));

    Path expectedPath = Paths.get("src", "test", "resources", "sorted.tsv");
    String expected =
        Files.readString(expectedPath, StandardCharsets.UTF_8)
            .replaceAll("\\n|\\r\\n", System.getProperty("line.separator"));

    assertEquals(expected, actual);
  }

  @Test
  void sortTsvFileNotFound() {
    TsvSorter tsvSorter = new TsvSorterImpl();
    Path inputPath = Path.of("unknown");
    Path outputPath = Path.of("unknown-output");
    assertThrows(UncheckedIOException.class, () -> tsvSorter.sortTsv(inputPath, outputPath));
  }
}
