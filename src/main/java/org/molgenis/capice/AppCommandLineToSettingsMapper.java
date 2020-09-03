package org.molgenis.capice;

import static org.molgenis.capice.AppCommandLineOptions.OPT_FORCE;
import static org.molgenis.capice.AppCommandLineOptions.OPT_INPUT;
import static org.molgenis.capice.AppCommandLineOptions.OPT_OUTPUT;
import static org.molgenis.capice.AppCommandLineOptions.OPT_TYPE;

import java.nio.file.Path;
import org.apache.commons.cli.CommandLine;
import org.molgenis.capice.vcf.Settings;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class AppCommandLineToSettingsMapper {

  private final String appName;
  private final String appVersion;

  AppCommandLineToSettingsMapper(
      @Value("${app.name}") String appName, @Value("${app.version}") String appVersion) {
    this.appName = appName;
    this.appVersion = appVersion;
  }

  Settings map(CommandLine commandLine) {
    String inputPathValue = commandLine.getOptionValue(OPT_INPUT);
    Path inputPath = Path.of(inputPathValue);

    Path outputPath;
    if (commandLine.hasOption(OPT_OUTPUT)) {
      outputPath = Path.of(commandLine.getOptionValue(OPT_OUTPUT));
    } else {
      outputPath = Path.of(commandLine.getOptionValue(OPT_INPUT) + ".vcf.gz");
    }

    boolean overwriteOutput = commandLine.hasOption(OPT_FORCE);

    FileType fileType;
    if (commandLine.hasOption(OPT_TYPE)) {
      String optionStr = commandLine.getOptionValue(OPT_TYPE);
      switch (optionStr) {
        case "precomputed_scores":
          fileType = FileType.PRECOMPUTED_SCORES;
          break;
        case "predictions":
          fileType = FileType.PREDICTIONS;
          break;
        default:
          throw new IllegalArgumentException(String.format("invalid file type '%s'", optionStr));
      }
    } else {
      fileType = FileType.PREDICTIONS;
    }
    return new Settings(inputPath, outputPath, overwriteOutput, fileType, appName, appVersion);
  }
}
