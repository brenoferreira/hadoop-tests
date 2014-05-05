import com.twitter.scalding._

class NGramsJob(args: Args) extends Job(args) {
  val regex = "^[A-Za-z+'-]+$"
  
  TextLine(args("input"))
  	.map('line -> 'values){ line:String => line.split("\t") }
  	.mapTo('values -> ('ngram, 'decade, 'occurrences)) { values:Array[String] => ( values(0), getDecade(values(1)).toInt, values(2).toInt ) }
  	.filter( ('ngram, 'decade) ) { x:(String, Int) => x._2 > 190 && x._1.matches(regex)  }
  	.groupBy( 'ngram, 'decade ) { _.sum[Int]('occurrences) }
  	.write( Tsv(args("output")) )
  	
  def getDecade(year:String) = year.substring(0, 3)
}