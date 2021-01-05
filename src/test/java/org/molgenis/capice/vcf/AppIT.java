package org.molgenis.capice.vcf;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.molgenis.capice.vcf.utils.GzippedVcfUtil.getVcfGzAsString;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.molgenis.capice.App;
import org.springframework.boot.SpringApplication;
import org.springframework.util.ResourceUtils;

class AppIT {

  @TempDir Path sharedTempDir;

  @Test
  void testPredictions() throws IOException {
    String inputFile = ResourceUtils.getFile("classpath:input_predictions.tsv").toString();
    String outputFile = sharedTempDir.resolve("capice_predictions_actual.vcf.gz").toString();

    String[] args = {"-i", inputFile, "-o", outputFile, "-f"};
    SpringApplication.run(App.class, args);

    String actual = getVcfGzAsString(Path.of(outputFile)).replaceAll("##CAP=.*", "##CAP=test");
    Path expectedPath = Paths.get("src", "test", "resources", "capice_predictions.vcf");
    String expected =
        Files.readString(expectedPath, StandardCharsets.UTF_8)
            .replaceAll("\\n|\\r\\n", System.getProperty("line.separator"));

    assertEquals(expected, actual);
  }

  @Test
  void testPrecomputedScores() throws IOException {
    String inputFile = ResourceUtils.getFile("classpath:input_precomputed_scores.tsv").toString();
    String outputFile = sharedTempDir.resolve("capice_precomputed_scores_actual.vcf.gz").toString();

    String[] args = {"-i", inputFile, "-o", outputFile, "-f", "-t", "precomputed_scores"};
    SpringApplication.run(App.class, args);

    String actual = getVcfGzAsString(Path.of(outputFile)).replaceAll("##CAP=.*", "##CAP=test");
    Path expectedPath = Paths.get("src", "test", "resources", "capice_precomputed_scores.vcf");
    String expected =
        Files.readString(expectedPath, StandardCharsets.UTF_8)
            .replaceAll("\\n|\\r\\n", System.getProperty("line.separator"));

    assertEquals(expected, actual);
  }

  @Test
  void testPrecomputedScoresGzipped() throws IOException {
    String inputFile = ResourceUtils.getFile("classpath:input_precomputed_scores.tsv.gz").toString();
    String outputFile = sharedTempDir.resolve("capice_precomputed_scores_actual.vcf.gz").toString();

    String[] args = {"-i", inputFile, "-o", outputFile, "-f", "-t", "precomputed_scores"};
    SpringApplication.run(App.class, args);

    String actual = getVcfGzAsString(Path.of(outputFile)).replaceAll("##CAP=.*", "##CAP=test");
    Path expectedPath = Paths.get("src", "test", "resources", "capice_precomputed_scores.vcf");
    String expected =
        Files.readString(expectedPath, StandardCharsets.UTF_8)
            .replaceAll("\\n|\\r\\n", System.getProperty("line.separator"));

    assertEquals(expected, actual);
  }
}
