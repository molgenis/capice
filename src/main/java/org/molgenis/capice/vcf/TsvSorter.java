package org.molgenis.capice.vcf;

import java.io.File;
import java.nio.file.Path;

public interface TsvSorter {
  void sortTsv(Path inputTsv, Path outputTsv, File tempDir);
}
