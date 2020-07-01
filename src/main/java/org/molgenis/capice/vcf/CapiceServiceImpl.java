package org.molgenis.capice.vcf;

import static java.util.Objects.requireNonNull;

import java.nio.file.Path;
import org.springframework.stereotype.Component;

@Component
public class CapiceServiceImpl implements CapiceService {

  private final TsvSorter tsvSorter;
  private final TsvToVcfMapper tsvToVcfMapper;

  CapiceServiceImpl(TsvSorter tsvSorter, TsvToVcfMapper tsvToVcfMapper) {
    this.tsvSorter = requireNonNull(tsvSorter);
    this.tsvToVcfMapper = requireNonNull(tsvToVcfMapper);
  }

  @Override
  public void mapPredictionsToVcf(Settings settings) {
    Path inputTsvPath = settings.getInputTsvPath();
    Path sortedTsvPath = Path.of(inputTsvPath.toString() + ".sorted");
    tsvSorter.sortTsv(inputTsvPath, sortedTsvPath);

    tsvToVcfMapper.map(sortedTsvPath, settings.getOutputVcfPath());
  }
}
