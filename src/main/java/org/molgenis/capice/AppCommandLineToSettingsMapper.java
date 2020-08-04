package org.molgenis.capice;

import static org.molgenis.capice.AppCommandLineOptions.OPT_FORCE;
import static org.molgenis.capice.AppCommandLineOptions.OPT_INPUT;
import static org.molgenis.capice.AppCommandLineOptions.OPT_OUTPUT;
import static org.molgenis.capice.AppCommandLineOptions.OPT_TEMP;

import java.io.File;
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

    File tempDir = null;
    if (commandLine.hasOption(OPT_TEMP)) {
      tempDir = Path.of(commandLine.getOptionValue(OPT_TEMP)).toFile();
    }

    boolean overwriteOutput = commandLine.hasOption(OPT_FORCE);

    return new Settings(inputPath, outputPath, overwriteOutput, appName, appVersion, tempDir);
  }
}
