package org.molgenis.capice.vcf;

import static java.nio.charset.StandardCharsets.UTF_8;
import static java.util.Collections.singletonList;
import static org.molgenis.capice.vcf.CapiceUtils.getVcfPositionFromPrecomputedScore;
import static org.molgenis.capice.vcf.CapiceUtils.getVcfPositionFromPrediction;
import static org.molgenis.capice.vcf.TsvUtils.TSV_FORMAT;

import htsjdk.variant.variantcontext.VariantContextBuilder;
import htsjdk.variant.variantcontext.writer.VariantContextWriter;
import htsjdk.variant.variantcontext.writer.VariantContextWriterBuilder;
import htsjdk.variant.variantcontext.writer.VariantContextWriterBuilder.OutputType;
import htsjdk.variant.vcf.VCFHeader;
import htsjdk.variant.vcf.VCFHeaderLine;
import htsjdk.variant.vcf.VCFHeaderLineCount;
import htsjdk.variant.vcf.VCFHeaderLineType;
import htsjdk.variant.vcf.VCFInfoHeaderLine;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UncheckedIOException;
import java.nio.file.Path;
import java.util.Iterator;
import java.util.zip.GZIPInputStream;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.stereotype.Component;

@Component
public class TsvToVcfMapperImpl implements TsvToVcfMapper {
  private static final String INFO_ID_CAPICE = "CAP";
  public static final int POSITION_INDEX = 0;
  public static final int SCORE_INDEX = 4;

  @Override
  public void map(Path sortedTsvPath, Path outputVcfPath, Settings settings) {
    try (VariantContextWriter variantContextWriter = createVariantContextWriter(outputVcfPath)) {
      setVcfHeader(settings, variantContextWriter);
      mapCapicePredictionsOutput(sortedTsvPath, variantContextWriter);
    }
  }

  @Override
  public void mapPrecomputedScores(Path inputTsvPath, Path outputVcfPath, Settings settings) {
    try (VariantContextWriter variantContextWriter = createVariantContextWriter(outputVcfPath)) {
      setVcfHeader(settings, variantContextWriter);
      mapCapicePrecomputedScoresOutput(inputTsvPath, variantContextWriter);
    }
  }

  private void mapCapicePredictionsOutput(
      Path sortedTsvPath, VariantContextWriter variantContextWriter) {
    try (Reader in = createInputReader(sortedTsvPath);
        CSVParser csvParser = TSV_FORMAT.parse(in)) {
      Iterator<CSVRecord> iterator = csvParser.iterator();
      iterator.next(); // skip header line (TSV_FORMAT.withSkipHeaderLine doesn't seem to work)
      while (iterator.hasNext()) {
        CSVRecord record = iterator.next();
        mapPredictionsLine(variantContextWriter, record);
      }
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }
  }

  private void mapCapicePrecomputedScoresOutput(
      Path inputTsvPath, VariantContextWriter variantContextWriter) {
    try (Reader in = createInputReader(inputTsvPath);
        CSVParser csvParser = TSV_FORMAT.parse(in)) {
      for (CSVRecord record : csvParser) {
        mapPrecomputedScoreLine(variantContextWriter, record);
      }
    } catch (IOException e) {
      throw new UncheckedIOException(e);
    }
  }

  void mapPredictionsLine(VariantContextWriter variantContextWriter, CSVRecord record) {
    validateLine(record);
    VcfPosition vcfPosition = getVcfPositionFromPrediction(record);
    float prediction = getPrediction(record);

    map(vcfPosition, prediction, variantContextWriter);
  }

  private void mapPrecomputedScoreLine(
      VariantContextWriter variantContextWriter, CSVRecord record) {
    VcfPosition vcfPosition = getVcfPositionFromPrecomputedScore(record);
    float prediction = getPrediction(record);

    map(vcfPosition, prediction, variantContextWriter);
  }

  private void map(
      VcfPosition vcfPosition, float prediction, VariantContextWriter variantContextWriter) {
    long start = vcfPosition.getPosition();
    long stop = start + (vcfPosition.getReference().length() - 1);
    VariantContextBuilder variantContextBuilder = new VariantContextBuilder();
    variantContextBuilder.chr(vcfPosition.getChromosome());
    variantContextBuilder.start(start);
    variantContextBuilder.stop(stop);
    variantContextBuilder.alleles(vcfPosition.getReference(), vcfPosition.getAlternative());
    variantContextBuilder.attribute(INFO_ID_CAPICE, singletonList(prediction));
    variantContextWriter.add(variantContextBuilder.make());
  }

  private void validateLine(CSVRecord record) {
    if (record.get(POSITION_INDEX) == null || record.get(SCORE_INDEX) == null) {
      throw new MalformedCapiceInputException(record.getRecordNumber());
    }
  }

  private void setVcfHeader(Settings settings, VariantContextWriter variantContextWriter) {
    VCFHeaderLineCount vcfHeaderLineCount = VCFHeaderLineCount.A;
    VCFHeaderLineType vcfHeaderLineType = VCFHeaderLineType.Float;
    String description = "CAPICE pathogenicity prediction";
    VCFInfoHeaderLine capiceVcfHeaderLine =
        new VCFInfoHeaderLine(INFO_ID_CAPICE, vcfHeaderLineCount, vcfHeaderLineType, description);
    VCFHeaderLine appVcfHeaderLine = new VCFHeaderLine("CAP", settings.getAppVersion());
    VCFHeader vcfHeader = new VCFHeader();
    vcfHeader.addMetaDataLine(appVcfHeaderLine);
    vcfHeader.addMetaDataLine(capiceVcfHeaderLine);

    variantContextWriter.writeHeader(vcfHeader);
  }

  private float getPrediction(CSVRecord record) {
    try {
      return Float.parseFloat(record.get(4));
    } catch (NumberFormatException e) {
      throw new IllegalStateException(e);
    }
  }

  private static Reader createInputReader(Path inputTsvPath) throws IOException {
    if (inputTsvPath.endsWith(".gz")) {
      return new InputStreamReader(
          new GZIPInputStream(new FileInputStream(inputTsvPath.toFile())), UTF_8);
    } else {
      return new InputStreamReader(new FileInputStream(inputTsvPath.toFile()), UTF_8);
    }
  }

  private static VariantContextWriter createVariantContextWriter(Path outputVcfPath) {
    return new VariantContextWriterBuilder()
        .setOutputFile(outputVcfPath.toFile())
        .setOutputFileType(OutputType.BLOCK_COMPRESSED_VCF)
        .build();
  }
}
