package org.molgenis.capice.vcf;

import java.nio.file.Path;
import lombok.NonNull;
import lombok.Value;
import lombok.experimental.NonFinal;

@Value
@NonFinal
public class Settings {
  @NonNull Path inputTsvPath;
  @NonNull Path outputVcfPath;
  boolean overwriteOutputVcf;
  @NonNull String appName;
  @NonNull String appVersion;
}
