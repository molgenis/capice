package org.molgenis.capice.vcf;

import java.nio.file.Path;

public interface TsvToVcfMapper {
  void map(Path sortedTsvPath, Path outputVcfPath);
}
