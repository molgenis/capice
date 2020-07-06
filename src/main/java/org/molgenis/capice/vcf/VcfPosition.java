package org.molgenis.capice.vcf;

import java.util.regex.Pattern;
import lombok.Data;
import lombok.NonNull;

@Data
public class VcfPosition {
  @NonNull private final String chromosome;
  @NonNull private final int position;

  public boolean isNumericChromosome(){
    return Pattern.compile("\\d+").matcher(chromosome).matches();
  }
}
