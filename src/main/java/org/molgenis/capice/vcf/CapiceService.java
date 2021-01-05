package org.molgenis.capice.vcf;

public interface CapiceService {
  void mapPredictionsToVcf(Settings settings);

  void mapPrecomputedScores(Settings settings);
}
