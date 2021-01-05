package org.molgenis.capice.vcf;

import java.nio.file.Path;
import lombok.NonNull;
import lombok.Value;
import lombok.experimental.NonFinal;
import org.molgenis.capice.FileType;

@Value
@NonFinal
public class Settings {
  @NonNull Path inputTsvPath;
  @NonNull Path outputVcfPath;
  boolean overwriteOutputVcf;
  FileType fileType;
  @NonNull String appName;
  @NonNull String appVersion;
}
