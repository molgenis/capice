package org.molgenis.capice.vcf;

import java.nio.file.Path;

public interface TsvToVcfMapper {
  void map(Path sortedTsvPath, Path outputVcfPath, Settings settings);

  void mapPrecomputedScores(Path inputTsvPath, Path outputVcfPath, Settings settings);
}
