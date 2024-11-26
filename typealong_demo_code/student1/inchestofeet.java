// Tyler Conlin
// 9-7-2024
// P1
// InchesToFeet.java
// This converts the number of inches input to the equivalent amount of 
// feet with decimals formated to two places
// numbers: 27, 24, and 0 will be used to test if it works, if it does
// the answers should be: 2.25, 2, and 0
// Working on: Using scanner and the appropriate method to read input

/* import Scanner class
 * class header
 * main header
 * construct scanner object console
 * 
 * print 3 BLs
 * provid prompt to input inches
 * D&I numOfInch, set to -1
 * use method nextInt to request input
 * 
 * D&I numOfFoot, set to -1.0f
 * set numOfFoot to numOfInch/12, maybe add parenthesis bc yus
 * 
 * Print sentence that tells reader how many feet the inches are 
 * converted to.
 * Use printf to control amount of decimals
 * 3 BLs
 */

import java.util.Scanner;

public class InchesToFeet
{
	public static void main (String [] args)
	{
		Scanner console = new Scanner( System.in );
		
		System.out.print("\n\n\n"); //laskdjflkasjdf
		System.out.print( "Input number of inches (whole" +
			" numbers only) -> " );
		int numOfInch;
		numOfInch = -1;
		numOfInch = console.nextInt( );
			
		float numOfFeet;
		numOfFeet = -1.0f;
		numOfFeet = numOfInch/12.0f;
		
		System.out.print(numOfInch + " inches is equivalent to");
		System.out.printf("%5.2f feet", numOfFeet);
	
		System.out.print("\n\n\n");
	}
}
