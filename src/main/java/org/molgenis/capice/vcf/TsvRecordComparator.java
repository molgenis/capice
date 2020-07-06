package org.molgenis.capice.vcf;

import java.util.Comparator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.commons.csv.CSVRecord;

public class TsvRecordComparator implements Comparator<CSVRecord> {
  private static final Pattern POS_PATTERN = Pattern.compile("(.+?)_(.+?)_.+?_.+?");


  @Override
  public int compare(CSVRecord thisRecord, CSVRecord thatRecord) {
    VcfPosition thisPosition = getVcfPosition(thisRecord);
    VcfPosition thatPosition = getVcfPosition(thatRecord);

    if (thisPosition.isNumericChromosome()) {
      return compareNumericChrom(thisPosition.getChromosome(), thisPosition.getPosition(), thatPosition.getChromosome(), thatPosition.isNumericChromosome(), thatPosition.getPosition());
    } else {
      if (thatPosition.isNumericChromosome()) {
        return 1;
      } else {
        return compareOtherChrom(thisPosition.getChromosome(), thisPosition.getPosition(), thatPosition.getChromosome(), thatPosition.getPosition());
      }
    }
  }

  private VcfPosition getVcfPosition(CSVRecord thatRecord) {
    String positionString = thatRecord.get(0);
    Matcher thatMatcher = POS_PATTERN.matcher(positionString);
    if (!thatMatcher.matches()) {
      throw new PositionParseException(positionString);
    }
    String thatChr = thatMatcher.group(1);
    int thatPos = Integer.parseInt(thatMatcher.group(2));
    return new VcfPosition(thatChr, thatPos);
  }

  private int compareOtherChrom(String thisChr, int thisPos, String thatChr, int thatPos) {
    if (thisChr.equals(thatChr)) {
      return thisPos - thatPos;
    } else {
      switch (thisChr) {
        case "X":
          return -1;
        case "Y":
          return thatChr.equals("X") ? 1 : -1;
        case "MT":
          return thatChr.equals("X") || thatChr.equals("Y") ? 1 : -1;
        default:
          return thatChr.equals("X") || thatChr.equals("Y") || thatChr.equals("MT")
              ? 1
              : thisChr.compareTo(thatChr);
      }
    }
  }

  private int compareNumericChrom(String thisChr, int thisPos, String thatChr,
      boolean thatChrIsNumber, int thatPos) {
    if (thatChrIsNumber) {
      int thisChrNr = Integer.parseInt(thisChr);
      int thatChrNr = Integer.parseInt(thatChr);
      if (thisChrNr == thatChrNr) {
        return thisPos - thatPos;
      } else {
        return thisChrNr - thatChrNr;
      }
    } else {
      return -1;
    }
  }
}
