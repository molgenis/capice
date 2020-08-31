package org.molgenis.capice.vcf;

import static java.util.Objects.requireNonNull;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Component
public class CapiceServiceImpl implements CapiceService {
  private static final Logger LOGGER = LoggerFactory.getLogger(CapiceServiceImpl.class);

  private final TsvSorter tsvSorter;
  private final TsvToVcfMapper tsvToVcfMapper;

  CapiceServiceImpl(TsvSorter tsvSorter, TsvToVcfMapper tsvToVcfMapper) {
    this.tsvSorter = requireNonNull(tsvSorter);
    this.tsvToVcfMapper = requireNonNull(tsvToVcfMapper);
  }

  @Override
  public void mapPredictionsToVcf(Settings settings) {
    Path inputTsvPath = settings.getInputTsvPath();
    Path sortedTsvPath = null;
    try {
      LOGGER.info("sorting tsv ...");
      sortedTsvPath = Files.createTempFile(null, null);
      tsvSorter.sortTsv(inputTsvPath, sortedTsvPath);
      LOGGER.info("done sorting tsv");

      LOGGER.info("mapping tsv to vcf...");
      tsvToVcfMapper.map(sortedTsvPath, settings.getOutputVcfPath(), settings);
      LOGGER.info("done mapping tsv to vcf");
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    } finally {
      if (sortedTsvPath != null) {
        try {
          Files.delete(sortedTsvPath);
        } catch (IOException e) {
          LOGGER.warn("unable to delete temporary file '{}'", sortedTsvPath);
        }
      }
    }
  }

  @Override
  public void mapPrecomputedScores(Settings settings) {
    Path inputTsvPath = settings.getInputTsvPath();

    LOGGER.info("mapping tsv to vcf...");
    tsvToVcfMapper.mapPrecomputedScores(inputTsvPath, settings.getOutputVcfPath(), settings);
    LOGGER.info("done mapping tsv to vcf");
  }
}
