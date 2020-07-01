package org.molgenis.capice.vcf;

import java.nio.file.Path;
import lombok.NonNull;
import lombok.Value;
import lombok.experimental.NonFinal;

@Value
@NonFinal
public class Settings {
  @NonNull Path inputVcfPath;
  @NonNull Path outputReportPath;
  boolean overwriteOutputReport;
  @NonNull String appName;
  @NonNull String appVersion;
}
