package org.molgenis.capice.vcf;

import java.util.Comparator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.commons.csv.CSVRecord;

public class TsvRecordComparator implements Comparator<CSVRecord> {
  private static final Pattern POS_PATTERN = Pattern.compile("(.+?)_(.+?)_.+?_.+?");
  private static final Pattern NUMBER_PATTERN = Pattern.compile("\\d+");

  @Override
  public int compare(CSVRecord thisRecord, CSVRecord thatRecord) {
    Matcher thisMatcher = POS_PATTERN.matcher(thisRecord.get(0));
    if (!thisMatcher.matches()) {
      throw new RuntimeException("todo");
    }
    String thisChr = thisMatcher.group(1);
    boolean thisChrIsNumber = NUMBER_PATTERN.matcher(thisChr).matches();
    int thisPos = Integer.parseInt(thisMatcher.group(2));

    Matcher thatMatcher = POS_PATTERN.matcher(thatRecord.get(0));
    if (!thatMatcher.matches()) {
      throw new RuntimeException("todo");
    }
    String thatChr = thatMatcher.group(1);
    boolean thatChrIsNumber = NUMBER_PATTERN.matcher(thatChr).matches();
    int thatPos = Integer.parseInt(thatMatcher.group(2));

    if (thisChrIsNumber) {
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
    } else {
      if (thatChrIsNumber) {
        return 1;
      } else {
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
    }
  }
}
