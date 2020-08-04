package org.molgenis.capice.vcf;

import static org.junit.jupiter.api.Assertions.*;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class TsvSorterImplTest {

  @TempDir
  static Path sharedTempDir;

  @Test
  void sortTsv() throws IOException {

    Path inputPath = Paths.get("src", "test", "resources", "input.tsv");
    Path outputPath = sharedTempDir.resolve("output.tsv");

    TsvSorter tsvSorter = new TsvSorterImpl();

    tsvSorter.sortTsv(inputPath, outputPath, sharedTempDir.toFile());

    String actual = Files.readString(outputPath, StandardCharsets.UTF_8);

    Path expectedPath = Paths.get("src", "test", "resources", "sorted.tsv");
    String expected = Files.readString(expectedPath, StandardCharsets.UTF_8);

    assertEquals(expected, actual);
  }
}