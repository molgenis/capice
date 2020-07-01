package org.molgenis.capice.vcf;

import java.nio.file.Path;
import org.springframework.stereotype.Component;

@Component
public class TsvToVcfMapperImpl implements TsvToVcfMapper {

  @Override
  public void map(Path sortedTsvPath, @NonNull Path outputVcfPath) {

  }
}
