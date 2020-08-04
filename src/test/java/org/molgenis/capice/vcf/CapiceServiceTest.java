package org.molgenis.capice.vcf;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.io.TempDir;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
class CapiceServiceTest {
  @Mock
  private TsvSorter tsvSorter;
  @Mock private TsvToVcfMapper tsvToVcfMapper;
  private CapiceService capiceService;

  @TempDir
  static Path sharedTempDir;

  @BeforeEach
  void setUpBeforeEach() {
    capiceService =
        new CapiceServiceImpl(tsvSorter, tsvToVcfMapper);
  }
  @Test
  void mapPredictionsToVcf() throws IOException {
    Path inputPath = Paths.get("src", "test", "resources", "input.tsv");
    Path outputVcfPath = sharedTempDir.resolve("output.vcf.gz");

    Settings settings = new Settings(inputPath,outputVcfPath,true,"capice2vcf", "test", null);
    capiceService.mapPredictionsToVcf(settings);

    verify(tsvSorter).sortTsv(eq(inputPath),any(),eq(null));
    verify(tsvToVcfMapper).map(any(),eq(outputVcfPath),eq(settings));
  }
}